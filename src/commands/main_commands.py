
from twitchAPI.chat import ChatCommand

from src.utils import cooldown

class MainCommands:
    @cooldown(10, True)
    async def commands_command_handler(self, cmd: ChatCommand):
        await cmd.reply("!тг, !гайд, !мейн, !монетка, !ролл, !шар (вопрос)")
    
    @cooldown(30, True)
    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("https://t.me/alaquu")
        else:
            if int(cmd.parameter) <= 5:
                for _ in range(int(cmd.parameter)):
                    await cmd.reply("https://t.me/alaquu")
            else:
                await cmd.reply("Дохуя просишь братик) https://t.me/alaquu")
    
    @cooldown(30, True)  
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Гайд на кеза и тинкера - https://t.me/alaquu/460")
    
    @cooldown(30, True)
    async def main_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Мейн Егора - https://steamcommunity.com/profiles/76561198993439266")