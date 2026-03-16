import asyncio
import os
from pathlib import Path
from functools import partial

from twitchAPI.type import ChatEvent, TwitchBackendException

from src.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    CHANNELS,
    TOKEN,
    REFRESH_TOKEN,
)
from src.adapters.api.client import APIClient
from src.adapters.twitch.client import TwitchClient
from src.adapters.twitch.settings import TWITCH_SCOPES

from src.services.auth import AuthService
from src.services.cooldown import CooldownService
from src.services.plugin_manager import PluginManager

from src.handlers.events import on_message as message_handler, on_ready

from src.handlers.eventsub import EventSubManager
from src.handlers.eventsub import follow, subscribe, gift, raid, stream

from src.utils.logger import logger


class Bot:
    _api_client: APIClient | None
    _twitch_client: TwitchClient | None
    _auth_service: AuthService | None
    _cooldown_service: CooldownService | None
    _plugin_manager: PluginManager | None
    _eventsub_manager: EventSubManager | None

    def __init__(
        self, shutdown_event: asyncio.Event, api_client: APIClient | None = None
    ) -> None:
        self._shutdown_event = shutdown_event
        self._stop_event: asyncio.Event | None = None
        self._api_client_provided = api_client is not None
        object.__setattr__(self, "_api_client", api_client)

        self._plugin_manager = None

    @staticmethod
    def _create_auth_service() -> AuthService:
        env_path_str = os.environ.get("ENV_PATH")
        if env_path_str:
            env_path = Path(env_path_str)
        else:
            env_path = Path(__file__).parent.parent / ".env"

        auth = AuthService(env_path)
        auth.load_tokens(TOKEN, REFRESH_TOKEN)
        return auth

    @staticmethod
    def _create_cooldown_service() -> CooldownService:
        CooldownService.reset_instance()
        return CooldownService()

    def _create_api_client(self) -> APIClient:
        if self._api_client is None:
            self._api_client = APIClient()
        return self._api_client

    @staticmethod
    def _create_twitch_client(auth: AuthService) -> TwitchClient:
        return TwitchClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            auth_service=auth,
            scope=TWITCH_SCOPES,
        )

    def _create_plugin_manager(
        self,
        api_client: APIClient,
        twitch_client: TwitchClient,
        cooldown: CooldownService,
    ) -> PluginManager:
        return PluginManager(api_client, twitch_client, cooldown)

    def _register_events(self, twitch: TwitchClient) -> None:
        twitch.register_event(
            ChatEvent.MESSAGE,
            partial(message_handler, client=self._api_client),  # type: ignore[arg-type]
        )
        twitch.register_event(ChatEvent.READY, partial(on_ready, channels=CHANNELS))

    def _initialize_services(self) -> None:
        self._auth_service = self._create_auth_service()
        self._cooldown_service = self._create_cooldown_service()
        self._create_api_client()
        self._twitch_client = self._create_twitch_client(self._auth_service)
        self._plugin_manager = self._create_plugin_manager(
            self._api_client, self._twitch_client, self._cooldown_service  # type: ignore[arg-type]
        )

    async def _start_twitch(self) -> None:
        await self._twitch_client.initialize()

        loaded_plugins = self._plugin_manager.load_all()

        for plugin in loaded_plugins:
            await plugin.on_load()

        main_plugin = self._plugin_manager.get_plugins().get("main")
        if main_plugin and len(loaded_plugins) > 1:
            main_plugin.set_groups(loaded_plugins)

        self._plugin_manager.register_all_commands()

        self._register_events(self._twitch_client)  # type: ignore[arg-type]

        self._twitch_client.set_stop_event(self._stop_event)  # type: ignore[arg-type]
        await self._twitch_client.start()  # type: ignore[arg-type]

        self._eventsub_manager = EventSubManager(
            self._twitch_client._twitch,  # type: ignore[attr-defined]
            CHANNELS,
            self._twitch_client.chat,  # type: ignore[attr-defined]
        )
        self._eventsub_manager.register_callback("follow", follow.on_follow)
        self._eventsub_manager.register_callback("subscribe", subscribe.on_subscribe)
        self._eventsub_manager.register_callback("gift", gift.on_gift)
        self._eventsub_manager.register_callback("raid", raid.on_raid)
        self._eventsub_manager.register_callback(
            "stream_online", stream.on_stream_online
        )
        self._eventsub_manager.register_callback(
            "stream_offline", stream.on_stream_offline
        )
        await self._eventsub_manager.start()

    async def _cleanup(self) -> None:
        if self._stop_event:
            self._stop_event.set()

        if self._eventsub_manager:
            await self._eventsub_manager.stop()

        if self._plugin_manager:
            await self._plugin_manager.unload_all()

        if self._twitch_client:
            self._twitch_client.clear_handlers()
            self._twitch_client.stop()
            await self._twitch_client.close()

        if self._api_client and not self._api_client_provided:
            await self._api_client.close()
            object.__setattr__(self, "_api_client", None)

    def stop(self) -> None:
        self._shutdown_event.set()
        if self._stop_event:
            self._stop_event.set()

    async def run(self) -> None:
        while True:
            self._stop_event = asyncio.Event()

            try:
                logger.info("init")
                self._initialize_services()

                await self._api_client.load_data()
                await self._start_twitch()

                await self._stop_event.wait()
            except TwitchBackendException as e:
                logger.warning(f"Twitch connection lost: {e}, retrying in 60s...")
                await self._cleanup()
                await asyncio.sleep(60)
                continue
            except asyncio.CancelledError:
                self._shutdown_event.set()
                raise
            except Exception as e:
                error_type = type(e).__name__
                logger.exception(error_type, exc=e)
                logger.info("restart")
            finally:
                await self._cleanup()

            if self._shutdown_event.is_set():
                logger.info("shutdown complete")
                break

            await asyncio.sleep(15)
