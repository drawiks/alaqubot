from random import choice, randint
from src.core.plugin import Plugin


class FunPlugin(Plugin):
    name = "fun"
    version = "1.0.0"

    async def on_load(self) -> None:
        pass

    async def on_unload(self) -> None:
        pass

    def get_commands(self) -> list[dict]:
        return [
            {
                "name": "спин",
                "handler": self.spin,
                "config": self.get_command_config("спин"),
            },
            {
                "name": "ролл",
                "handler": self.roll,
                "config": self.get_command_config("ролл"),
            },
            {
                "name": "зона",
                "handler": self.zone,
                "config": self.get_command_config("зона"),
            },
            {
                "name": "шар",
                "handler": self.ball,
                "config": self.get_command_config("шар"),
            },
        ]

    @staticmethod
    async def spin(cmd):
        symbols = ["🍎", "🍒", "🍌", "🍉", "⭐"]

        if choice([True, False]):
            symbol = choice(symbols)
            await cmd.reply(f"Слоты: {symbol} {symbol} {symbol}")
        else:
            spin_result = [choice(symbols) for _ in range(3)]
            await cmd.reply(f"Слоты: {' '.join(spin_result)}")

    @staticmethod
    async def roll(cmd):
        await cmd.reply(str(randint(0, 100)))

    async def zone(self, cmd):
        words = self.settings.get("zones", [])
        await cmd.reply(choice(words) if words else "тихоня")

    @staticmethod
    async def ball(cmd):
        if not cmd.parameter:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(
                choice(
                    [
                        "Да",
                        "Нет",
                        "Точно да",
                        "Точно нет",
                        "Неуверен",
                        "Наверное",
                        "Не сейчас",
                        "Спроси снова",
                    ]
                )
            )
