
from twitchAPI.chat import ChatCommand

from random import randint, choice

from src.utils import Commands, register, cooldown

class FunCommands(Commands):
    """!спин"""
    @register("спин")
    @cooldown(20)
    async def spin_command_handler(self, cmd: ChatCommand):
        users = self.client.users
        if cmd.user.name in users:
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
    
    """!ролл"""
    @register("ролл")
    @cooldown(10)
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(str(randint(0, 100)))
        
    """!зона"""
    @register("зона")
    @cooldown(10)
    async def zone_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["тихоня", "лох", "мент", "шестерка", "авторитет", "блатной", "вор в законе", "опущенный", "мастер на все руки", "пахан", "крыша", "туз", "бригадир", "приблатнённый", "фуфлыжник", "серый кардинал"]))
    
    """!шар"""
    @register("шар")
    @cooldown(30)
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))