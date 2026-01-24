
from twitchAPI.chat import ChatCommand
from src.utils import register, cooldown, get_commands, load_commands


class MainCommands:
    def __init__(self):
        self.commands = load_commands()
    
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
                channel = self.commands.get(cmd.room.name, {})
                await cmd.reply(channel.get("тг"))
                        
        else:
            if cmd.room is not None:
                channel = self.commands.get(cmd.room.name, {})
                if int(cmd.parameter) <= 5:
                    for _ in range(int(cmd.parameter)):
                        await cmd.reply(channel.get("тг"))
                else:
                    await cmd.reply("Дохуя просишь братик)")
    
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
        if cmd.room is not None:
            channel = self.commands.get(cmd.room.name, {})
            await cmd.reply(channel.get("гайд"))
    
    """!мейн"""
    @register("мейн")
    @cooldown(30)
    async def main_command_handler(self, cmd: ChatCommand):
        if cmd.room is not None:
            channel = self.commands.get(cmd.room.name, {})
            await cmd.reply(channel.get("мейн"))
        