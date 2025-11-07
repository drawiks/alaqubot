
from twitchAPI.chat import ChatCommand
from src.utils import register
class MainCommands:
    """!команды"""
    @register("команды")
    async def commands_command_handler(self, cmd: ChatCommand):
        await cmd.reply("!тг, !гайд, !мейн, !автор, !монетка, !ролл, !факт, !шар (вопрос), !карты (количество), !доллар (количество), !гороскоп (знак зодиака), !погода (город), !перевод (текст)")
    
    """!тг"""
    @register("тг")
    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("https://t.me/alaquu")
        else:
            if int(cmd.parameter) <= 5:
                for _ in range(int(cmd.parameter)):
                    await cmd.reply("https://t.me/alaquu")
            else:
                await cmd.reply("Дохуя просишь братик) https://t.me/alaquu")
    
    """!автор"""
    @register("автор")
    async def author(self, cmd: ChatCommand):
        for _ in ["tv/drawksr", "tv/lgwxgk", "https://github.com/drawiks", "https://t.me/budni_uznika"]:
            await cmd.send(_)
    
    """!гайд"""
    @register("гайд")
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Гайд на кеза и тинкера - https://t.me/alaquu/460")
    
    """!мейн"""
    @register("мейн")
    async def main_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Мейн Егора - https://steamcommunity.com/profiles/76561198993439266")