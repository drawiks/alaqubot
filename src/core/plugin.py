from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from src.adapters.api.client import APIClient
    from src.adapters.twitch.client import TwitchClient


class Plugin(ABC):
    name: str = "base"
    version: str = "1.0.0"

    def __init__(
        self,
        api_client: "APIClient",
        config: dict,
        users: list[str],
        twitch_client: Optional["TwitchClient"] = None,
    ):
        self._api = api_client
        self._config = config
        self._users = users
        self._twitch = twitch_client

    @property
    def enabled(self) -> bool:
        return self._config.get("enabled", True)

    @property
    def client(self) -> "APIClient":
        return self._api

    @property
    def twitch(self) -> Optional["TwitchClient"]:
        return self._twitch

    @property
    def users(self) -> list[str]:
        return self._users

    @property
    def commands_config(self) -> dict:
        return self._config.get("commands", {})

    @property
    def settings(self) -> dict:
        return self._config.get("settings", {})

    def check_permission(self, username: str) -> bool:
        return username in self._users

    def get_command_config(self, cmd_name: str) -> dict:
        return self.commands_config.get(cmd_name, {})

    def set_groups(self, groups: list["Plugin"]) -> None:
        pass

    async def on_load(self) -> None:
        pass

    async def on_unload(self) -> None:
        pass

    @abstractmethod
    def get_commands(self) -> list[dict]:
        pass
