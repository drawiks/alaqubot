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
        if not cmd.parameter:
            if cmd.room:
                channel = self.client.commands.get(cmd.room.name, {})
                link = channel.get("тг")
                if link:
                    await cmd.reply(link)
        else:
            if cmd.room:
                channel = self.client.commands.get(cmd.room.name, {})
                link = channel.get("тг")
                if not link:
                    await cmd.reply("Ссылка не настроена")
                    return
                try:
                    count = int(cmd.parameter)
                    if count <= 0:
                        await cmd.reply("Введи число больше 0!")
                        return
                    if count > 5:
                        await cmd.reply("Дохуя просишь братик)")
                        return
                    for _ in range(count):
                        await cmd.reply(link)
                except ValueError:
                    await cmd.reply("Введи число!")

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
            text = channel.get("гайд")
            if text:
                await cmd.reply(text)

    async def main(self, cmd):
        if cmd.room:
            channel = self.client.commands.get(cmd.room.name, {})
            text = channel.get("мейн")
            if text:
                await cmd.reply(text)
