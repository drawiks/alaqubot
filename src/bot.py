import asyncio
import importlib
import os
from pathlib import Path
from typing import Optional
from functools import wraps, partial

from twitchAPI.type import ChatEvent, TwitchBackendException

from src.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    CHANNELS,
    TOKEN,
    REFRESH_TOKEN,
    get_plugin_config,
)
from src.adapters.api.client import APIClient
from src.adapters.twitch.client import TwitchClient
from src.adapters.twitch.settings import TWITCH_SCOPES

from src.services.auth import AuthService
from src.services.cooldown import CooldownService

from src.core.plugin import Plugin

from src.handlers.events import on_message as message_handler, on_ready, message_cleanup

from src.utils.logger import logger


class Bot:
    _api_client: Optional[APIClient]
    _twitch_client: Optional[TwitchClient]
    _auth_service: Optional[AuthService]
    _cooldown_service: Optional[CooldownService]

    def __init__(
        self, shutdown_event: asyncio.Event, api_client: Optional[APIClient] = None
    ) -> None:
        self._shutdown_event = shutdown_event
        self._stop_event: Optional[asyncio.Event] = None
        self._api_client_provided = api_client is not None
        object.__setattr__(self, "_api_client", api_client)

        self._plugins: dict[str, Plugin] = {}

    @staticmethod
    def _discover_plugins() -> list[str]:
        plugins_path = Path(__file__).parent / "plugins"
        if not plugins_path.exists():
            return []

        return [
            name
            for name in os.listdir(plugins_path)
            if (plugins_path / name / "plugin.py").exists() and not name.startswith("_")
        ]

    def _load_plugin(self, name: str) -> Optional[Plugin]:
        try:
            module = importlib.import_module(f"src.plugins.{name}.plugin")
            plugin_class_name = f"{name.title()}Plugin"
            plugin_class = getattr(module, plugin_class_name)

            config = get_plugin_config(name)

            if not config.get("enabled", True):
                logger.info(f"Plugin {name} disabled in config")
                return None

            return plugin_class(self._api_client, config, self._api_client.users, self._twitch_client)  # type: ignore[union-attr]
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")
            return None

    def _register_plugin_commands(self, plugin: Plugin) -> None:
        for cmd in plugin.get_commands():
            config = cmd.get("config", {})

            if not config.get("enabled", True):
                continue

            handler = cmd["handler"]
            cmd_name = cmd["name"]

            if config.get("cooldown", 0) > 0:
                handler = self._wrap_with_cooldown(handler, config["cooldown"])

            self._twitch_client.register_command(cmd_name, handler)  # type: ignore[union-attr]
            logger.debug(f"command {cmd_name} registered from plugin {plugin.name}")

    @staticmethod
    def _wrap_with_cooldown(handler, cooldown_seconds: int):
        cooldown = CooldownService()

        @wraps(handler)
        async def wrapped(cmd):
            allowed, wait = cooldown.check(
                cmd.user.name, handler.__name__, cooldown_seconds
            )
            if not allowed:
                await cmd.reply(f"Подожди {round(wait, 1)} сек!")
                return

            cooldown.set(cmd.user.name, handler.__name__, cooldown_seconds)
            await handler(cmd)

        return wrapped

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

    async def _load_plugins(self) -> None:
        plugin_names = self._discover_plugins()
        logger.info(f"Discovered plugins: {plugin_names}")

        main_plugin = None

        for name in plugin_names:
            plugin = self._load_plugin(name)
            if plugin:
                await plugin.on_load()
                self._plugins[name] = plugin

                if name == "main":
                    main_plugin = plugin

        if main_plugin and len(self._plugins) > 1:
            all_plugins = list(self._plugins.values())
            main_plugin.set_groups(all_plugins)  # type: ignore[union-attr]

    async def _register_plugins(self) -> None:
        for _, plugin in self._plugins.items():
            self._register_plugin_commands(plugin)

    async def _start_twitch(self) -> None:
        await self._twitch_client.initialize()  # type: ignore[union-attr]

        await self._load_plugins()
        await self._register_plugins()

        self._register_events(self._twitch_client)  # type: ignore[arg-type]

        self._twitch_client.set_stop_event(self._stop_event)  # type: ignore[union-attr]
        await self._twitch_client.start()  # type: ignore[union-attr]

    async def _cleanup(self) -> None:
        if self._stop_event:
            self._stop_event.set()

        for name, plugin in self._plugins.items():
            try:
                await plugin.on_unload()
            except Exception as e:
                logger.error(f"Error unloading plugin {name}: {e}")

        self._plugins.clear()

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

                await self._api_client.load_data()  # type: ignore[union-attr]
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
