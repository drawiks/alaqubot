
from twitchAPI.chat import ChatCommand

from random import randint, choice

from src.utils import Cards, get_fact, register, cooldown
from src.api import load_users

class FunCommands:
    def __init__(self):
        self.cards = Cards()
        self.users = load_users()
    
    """!спин"""
    @register("спин")
    @cooldown(20)
    async def spin_command_handler(self, cmd: ChatCommand):
        if cmd.user.name in self.users["users"]:
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
    @register("карты")
    @cooldown(30)
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
    @register("факт")
    @cooldown(20)
    async def fact_command_handler(self, cmd: ChatCommand):
        await cmd.reply(get_fact())
    
    """!монетка"""
    @register("монетка")
    @cooldown(10)
    async def coin_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["Орёл", "Решка"]))
    
    """!ролл"""
    @register("ролл")
    @cooldown(10)
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(str(randint(0, 100)))
        
    """!зона"""
    @register("зона")
    @cooldown(10)
    async def zone_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["тихоня", "мент", "шестерка", "авторитет", "блатной", "вор в законе", "опущенный", "мастер на все руки", "пахан", "крыша", "туз", "бригадир", "приблатнённый", "фуфлыжник", "серый кардинал"]))
    
    """!удар"""
    @register("удар")
    @cooldown(10)
    async def punch_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши юзернейм!")
        else:
            await cmd.reply(f"Вы ударили - {cmd.parameter}")
    
    """!шар"""
    @register("шар")
    @cooldown(30)
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))