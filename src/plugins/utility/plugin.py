from datetime import datetime
from src.core.plugin import Plugin
from src.utils.uptime import get_uptime


class UtilityPlugin(Plugin):
    name = "utility"
    version = "1.0.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.now()

    async def on_load(self) -> None:
        pass

    async def on_unload(self) -> None:
        pass

    def get_commands(self) -> list[dict]:
        return [
            {
                "name": "доллар",
                "handler": self.converter,
                "config": self.get_command_config("доллар"),
            },
            {
                "name": "погода",
                "handler": self.weather,
                "config": self.get_command_config("погода"),
            },
            {
                "name": "фильм",
                "handler": self.film,
                "config": self.get_command_config("фильм"),
            },
            {"name": "wl", "handler": self.wl, "config": self.get_command_config("wl")},
            {
                "name": "mmr",
                "handler": self.mmr,
                "config": self.get_command_config("mmr"),
            },
            {
                "name": "setmmr",
                "handler": self.set_mmr,
                "config": self.get_command_config("setmmr"),
            },
            {
                "name": "setid",
                "handler": self.set_id,
                "config": self.get_command_config("setid"),
            },
            {
                "name": "uptime",
                "handler": self.uptime,
                "config": self.get_command_config("uptime"),
            },
            {
                "name": "email",
                "handler": self.email,
                "config": self.get_command_config("email"),
            },
        ]

    async def converter(self, cmd):
        if len(cmd.parameter) == 0:
            result = await self.client.request("currency")
        else:
            result = await self.client.request("currency", float(cmd.parameter))
        await cmd.reply(result)

    async def weather(self, cmd):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название города!")
        else:
            result = await self.client.request("weather", cmd.parameter)
            await cmd.reply(result)

    async def film(self, cmd):
        result = await self.client.request("film")
        await cmd.reply(result)

    async def wl(self, cmd):
        result = await self.client.request("wl", str(cmd.room.name))
        await cmd.reply(result)

    async def mmr(self, cmd):
        result = await self.client.request("get_mmr", str(cmd.room.name))
        await cmd.reply(result)

    async def set_mmr(self, cmd):
        if not self.check_permission(cmd.user.name):
            await cmd.reply("У тебя нет прав на эту команду!")
            return

        if cmd.parameter.lstrip("-").isdigit():
            response = await self.client.post_request(
                "set_mmr", {"username": cmd.room.name, "mmr": cmd.parameter}
            )
            await cmd.reply(response)
        else:
            await cmd.reply("Введи число!")

    async def set_id(self, cmd):
        if not self.check_permission(cmd.user.name):
            await cmd.reply("У тебя нет прав на эту команду!")
            return

        if cmd.parameter.lstrip("-").isdigit():
            response = await self.client.post_request(
                "set_id", {"username": cmd.room.name, "dota_id": cmd.parameter}
            )
            await cmd.reply(response)
        else:
            await cmd.reply("Введи айди!")

    async def uptime(self, cmd):
        if not self.check_permission(cmd.user.name):
            await cmd.reply("У тебя нет прав на эту команду!")
            return

        await cmd.reply(get_uptime(self.start_time))

    async def email(self, cmd):
        if not self.check_permission(cmd.user.name):
            await cmd.reply("У тебя нет прав на эту команду!")
            return

        email = await self.twitch.get_bot_email()  # type: ignore[union-attr]
        if email:
            await cmd.reply(f"Email бота: {email}")
        else:
            await cmd.reply("Не удалось получить email")
