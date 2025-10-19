
from twitchAPI.chat import ChatCommand

from random import randint, choice
import asyncio

class FunCommands:
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
            
    async def test(self, msg: ChatCommand):
        for _ in range(10):
            await msg.send("КАНАЛ ГДЕ ТРАХАЮТ ШКОЛЬНИЦ В ШАПКЕ ПРОФИЛЯ")
            await asyncio.sleep(0.2)
    
    async def coin_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["Орёл", "Решка"]))
    
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(randint(0, 100))
        
    async def punch_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши юзернейм!")
        else:
            await cmd.reply(f"Вы ударили - {cmd.parameter}")
    
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))