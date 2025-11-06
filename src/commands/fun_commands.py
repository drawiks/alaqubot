
from twitchAPI.chat import ChatCommand

from random import randint, choice

from src.utils import Cards, get_fact

class FunCommands:
    def __init__(self):
        self.cards = Cards()
    
    """!спин"""
    async def spin_command_handler(self, cmd: ChatCommand):
        if cmd.user.name in ["alaqu1337", "lgwxgk"]:
            if choice([True, False]):
                symbol = choice(["🍎", "🍒", "🍌", "🍉", "⭐"])
                text = f"Слоты: {symbol} {symbol} {symbol}"
                await cmd.reply(text)
            else:
                symbols = ["🍎", "🍒", "🍌", "🍉", "⭐"]
                spin = [choice(symbols) for _ in range(3)]
                text = f"Слоты: {spin[0]} {spin[1]} {spin[2]}"
                await cmd.reply(text)
        else:
            symbols = ["🍎", "🍒", "🍌", "🍉", "⭐"]
            spin = [choice(symbols) for _ in range(3)]
            text = f"Слоты: {spin[0]} {spin[1]} {spin[2]}"
            await cmd.reply(text)
    
    """!карты"""
    async def card_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            for _ in self.cards.get_cards():
                await cmd.reply(_)
        else:
            if int(cmd.parameter) <= 5:
                for _ in self.cards.get_cards(int(cmd.parameter)):
                    await cmd.reply(_)
            else:
                await cmd.reply("Дохуя просишь братик) https://t.me/alaquu")
    
    """!факт"""
    async def fact_command_handler(self, cmd: ChatCommand):
        await cmd.reply(get_fact())
    
    """!монетка"""
    async def coin_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["Орёл", "Решка"]))
    
    """!ролл"""
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(randint(0, 100))
    
    """!удар"""
    async def punch_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши юзернейм!")
        else:
            await cmd.reply(f"Вы ударили - {cmd.parameter}")
    
    """!шар"""
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))