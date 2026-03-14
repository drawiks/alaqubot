from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat
from twitchAPI.helper import first
from typing import Callable, Any, Optional
import asyncio

from src.utils.logger import logger
from src.services.auth import AuthService
from src.adapters.twitch.settings import DEFAULT_SCOPES


class TwitchClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        auth_service: AuthService,
        scope: Optional[list[AuthScope]] = None,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_service = auth_service
        self._scope = scope or DEFAULT_SCOPES

        self._twitch: Optional[Twitch] = None
        self._chat: Optional[Chat] = None
        self._stop_event: Optional[asyncio.Event] = None
        self._event_handlers: dict = {}
        self._command_handlers: dict = {}

    @property
    def chat(self) -> Optional[Chat]:
        return self._chat

    async def initialize(self) -> None:
        self._twitch = Twitch(self._client_id, self._client_secret)

        try:
            await self._twitch.set_user_authentication(
                self._auth_service.get_token(),
                self._scope,
                self._auth_service.get_refresh_token(),
            )
        except Exception as auth_err:
            logger.warning(f"auth error: {auth_err}, attempting token refresh")
            if await self._auth_service.refresh(self._client_id, self._client_secret):
                await self._twitch.set_user_authentication(
                    self._auth_service.get_token(),
                    self._scope,
                    self._auth_service.get_refresh_token(),
                )
            else:
                raise

        self._chat = await Chat(self._twitch)
        self._chat.no_message_reset_time = 5

    def register_event(self, event: ChatEvent, handler: Callable) -> None:
        if self._chat:
            self._chat.register_event(event, handler)

    def register_command(self, name: str, handler: Callable) -> None:
        if self._chat:
            self._command_handlers[name] = handler
            self._chat.register_command(name, handler)

    async def send_message(self, room: str, text: str) -> None:
        if self._chat:
            await self._chat.send_message(room, text)

    async def start(self) -> None:
        if self._chat:
            self._chat.start()

    def stop(self) -> None:
        if self._chat:
            self._chat.stop()

    async def close(self) -> None:
        if self._twitch:
            await self._twitch.close()

    async def wait(self) -> None:
        if self._stop_event:
            await self._stop_event.wait()

    def create_stop_event(self) -> asyncio.Event:
        self._stop_event = asyncio.Event()
        return self._stop_event

    def set_stop_event(self, event: asyncio.Event) -> None:
        self._stop_event = event

    def clear_handlers(self) -> None:
        self._event_handlers.clear()
        self._command_handlers.clear()

    async def get_bot_email(self) -> Optional[str]:
        if not self._twitch:
            return None
        user = await first(self._twitch.get_users())
        if user and hasattr(user, "email") and user.email:
            return user.email
        return None
