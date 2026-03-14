from src.core.plugin import Plugin


class MainPlugin(Plugin):
    name = "main"
    version = "1.0.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._groups = []

    def set_groups(self, groups: list):
        self._groups = groups

    async def on_load(self) -> None:
        pass

    async def on_unload(self) -> None:
        pass

    def get_commands(self) -> list[dict]:
        return [
            {
                "name": "команды",
                "handler": self.list_commands,
                "config": self.get_command_config("команды"),
            },
            {"name": "тг", "handler": self.tg, "config": self.get_command_config("тг")},
            {
                "name": "автор",
                "handler": self.author,
                "config": self.get_command_config("автор"),
            },
            {
                "name": "гайд",
                "handler": self.guide,
                "config": self.get_command_config("гайд"),
            },
            {
                "name": "мейн",
                "handler": self.main,
                "config": self.get_command_config("мейн"),
            },
        ]

    async def list_commands(self, cmd):
        names = []
        for group in self._groups:
            for cmd_dict in group.get_commands():
                config = cmd_dict.get("config", {})
                if (
                    config
                    and config.get("enabled", True)
                    and config.get("public", True)
                    and not config.get("requires_permission", False)
                ):
                    names.append(cmd_dict["name"])

        commands = sorted(list(set(names)))
        reply = "Команды: !" + ", !".join(commands)
        await cmd.reply(reply)

    async def tg(self, cmd):
        if len(cmd.parameter) == 0:
            if cmd.room:
                channel = self.client.commands.get(cmd.room.name, {})
                await cmd.reply(channel.get("тг"))
        else:
            if cmd.room:
                channel = self.client.commands.get(cmd.room.name, {})
                if int(cmd.parameter) <= 5:
                    for _ in range(int(cmd.parameter)):
                        await cmd.reply(channel.get("тг"))
                else:
                    await cmd.reply("Дохуя просишь братик)")

    @staticmethod
    async def author(cmd):
        for link in [
            "tv/drawksr",
            "tv/lgwxgk",
            "https://github.com/drawiks",
            "https://t.me/budni_uznika",
        ]:
            await cmd.send(link)

    async def guide(self, cmd):
        if cmd.room:
            channel = self.client.commands.get(cmd.room.name, {})
            await cmd.reply(channel.get("гайд"))

    async def main(self, cmd):
        if cmd.room:
            channel = self.client.commands.get(cmd.room.name, {})
            await cmd.reply(channel.get("мейн"))
