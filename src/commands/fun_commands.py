
from twitchAPI.chat import ChatCommand

from src.utils import cooldown

from random import randint, choice

class FunCommands:
    @cooldown(30, True)
    async def coin_command_handler(self, cmd: ChatCommand):
        await cmd.reply(choice(["Орёл", "Решка"]))
    
    @cooldown(30, True)
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(randint(0, 100))
    
    @cooldown(30, True)
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))