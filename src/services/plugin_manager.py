import importlib
import os
from functools import wraps
from pathlib import Path

from src.core.plugin import Plugin
from src.services.cooldown import CooldownService
from src.utils.logger import logger


class PluginManager:
    def __init__(
        self,
        api_client,
        twitch_client,
        cooldown_service: CooldownService,
    ):
        self._api = api_client
        self._twitch = twitch_client
        self._cooldown = cooldown_service
        self._plugins: dict[str, Plugin] = {}

    @staticmethod
    def discover() -> list[str]:
        plugins_path = Path(__file__).parent.parent / "plugins"
        if not plugins_path.exists():
            return []

        return [
            name
            for name in os.listdir(plugins_path)
            if (plugins_path / name / "plugin.py").exists() and not name.startswith("_")
        ]

    def load(self, name: str) -> Plugin | None:
        from src.config import get_plugin_config

        try:
            module = importlib.import_module(f"src.plugins.{name}.plugin")
            plugin_class_name = f"{name.title()}Plugin"
            plugin_class = getattr(module, plugin_class_name)

            config = get_plugin_config(name)

            if not config.get("enabled", True):
                logger.info(f"Plugin {name} disabled in config")
                return None

            return plugin_class(self._api, config, self._api.users, self._twitch)
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")
            return None

    def load_all(self) -> list[Plugin]:
        plugin_names = self.discover()
        logger.info(f"Discovered plugins: {plugin_names}")

        loaded = []
        for name in plugin_names:
            plugin = self.load(name)
            if plugin:
                self._plugins[name] = plugin
                loaded.append(plugin)

        return loaded

    def register_commands(self, plugin: Plugin) -> None:
        for cmd in plugin.get_commands():
            config = cmd.get("config", {})

            if not config.get("enabled", True):
                continue

            handler = cmd["handler"]
            cmd_name = cmd["name"]

            if config.get("cooldown", 0) > 0:
                handler = self.wrap_with_cooldown(handler, config["cooldown"])

            self._twitch.register_command(cmd_name, handler)
            logger.debug(f"command {cmd_name} registered from plugin {plugin.name}")

    def register_all_commands(self) -> None:
        for plugin in self._plugins.values():
            self.register_commands(plugin)

    def wrap_with_cooldown(self, handler, cooldown_seconds: int):
        @wraps(handler)
        async def wrapped(cmd):
            allowed, wait = self._cooldown.check(
                cmd.user.name, handler.__name__, cooldown_seconds
            )
            if not allowed:
                await cmd.reply(f"Подожди {round(wait, 1)} сек!")
                return

            self._cooldown.set(cmd.user.name, handler.__name__, cooldown_seconds)
            await handler(cmd)

        return wrapped

    async def unload_all(self) -> None:
        for name, plugin in self._plugins.items():
            try:
                await plugin.unload()
            except Exception as e:
                logger.error(f"Error unloading plugin {name}: {e}")

        self._plugins.clear()

    def get_plugins(self) -> dict[str, Plugin]:
        return self._plugins
