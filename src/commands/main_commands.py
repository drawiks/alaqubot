
from twitchAPI.chat import ChatCommand
from src.utils import register, cooldown, get_commands

class MainCommands:
    """!команды"""
    @register("команды")
    async def commands_command_handler(self, cmd: ChatCommand):
        all_cmds = get_commands().keys()
        reply = "Команды: !" + ", !".join(sorted(all_cmds))
        await cmd.reply(reply)
    
    """!тг"""
    @register("тг")
    @cooldown(30)
    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            if cmd.room is not None:
                match cmd.room.name:
                    case "alaqu1337":
                        await cmd.reply("https://t.me/alaquu")
                    case "paxi_pixi":
                        await cmd.reply("https://t.me/paxipixi")
        else:
            if cmd.room is not None and cmd.room.name == "alaqu1337":
                if int(cmd.parameter) <= 5:
                    for _ in range(int(cmd.parameter)):
                        await cmd.reply("https://t.me/alaquu")
                else:
                    await cmd.reply("Дохуя просишь братик) https://t.me/alaquu")
    
    """!автор"""
    @register("автор")
    @cooldown(20)
    async def author(self, cmd: ChatCommand):
        for _ in ["tv/drawksr", "tv/lgwxgk", "https://github.com/drawiks", "https://t.me/budni_uznika"]:
            await cmd.send(_)
    
    """!гайд"""
    @register("гайд")
    @cooldown(30)
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Гайд на кеза и тинкера - https://t.me/alaquu/460")
    
    """!мейн"""
    @register("мейн")
    @cooldown(30)
    async def main_command_handler(self, cmd: ChatCommand):
        if cmd.room is not None:
            match cmd.room.name:
                case "alaqu1337":
                    await cmd.reply("Мейн Егора - https://steamcommunity.com/profiles/76561198993439266")
                case "paxi_pixi":
                    await cmd.reply("Мейн Женька - 240695842")
        