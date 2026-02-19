
from twitchAPI.chat import ChatCommand

from datetime import datetime

from src.utils import Commands, register, cooldown, get_uptime

class UtilityCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.now()

    """!доллар"""
    @register("доллар")
    @cooldown(10)
    async def converter_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            result = await self.client.request("currency")
            await cmd.reply(result)
        else:
            result = await self.client.request("currency", float(cmd.parameter))
            await cmd.reply(result)
            
    """!гороскоп"""
    @register("гороскоп")
    @cooldown(30)
    async def horoscope_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи свой знак зодиака! (овен, телец, близнецы, рак, лев, дева, весы, скорпион, стрелец, козерог, водолей, рыбы)")
        else:
            result = await self.client.request("horoscope", str(cmd.parameter))
            await cmd.reply(result)
            
    """!фильм"""
    @register("фильм")
    @cooldown(30)
    async def film_command_handler(self, cmd: ChatCommand):
        result = await self.client.request("film")
        await cmd.reply(result)
        
    """!майнкрафт"""
    @register("майнкрафт")
    @cooldown(30)
    async def minecraft_command_handler(self, cmd: ChatCommand):
        result = await self.client.request("minecraft")
        await cmd.reply(result)
    
    """!погода"""
    @register("погода")
    @cooldown(10)
    async def weather_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название города!")
        else:
            result = await self.client.request("weather", str(cmd.parameter))
            await cmd.reply(result)
    
    """!перевод"""
    @register("перевод")
    @cooldown(10)
    async def translate_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи текст для перевода!")
        else:
            result = await self.client.request("translate", str(cmd.parameter))
            await cmd.reply(result)
    
    """!wl"""
    @register("wl")
    @cooldown(30)
    async def wl_command_handler(self, cmd: ChatCommand):
        result = await self.client.request("wl", str(cmd.room.name))
        await cmd.reply(result)
        
    """!mmr"""
    @register("mmr")
    @cooldown(10)
    async def mmr_command_handler(self, cmd: ChatCommand):
        result = await self.client.request("mmr", str(cmd.room.name))
        await cmd.reply(result)
        
    """!setmmr"""
    @register("setmmr", False)
    async def set_mmr_command_handler(self, cmd: ChatCommand):
        if cmd.user.name in self.client.users:
            if cmd.parameter.isdigit():
                response = await self.client.post_request("set_mmr", {"username": cmd.room.name, "mmr": cmd.parameter})
                await cmd.reply(response)
            else: await cmd.reply("Введи число!")
        else: await cmd.reply("У тебя нет прав на эту команду!")
            
    """!setid"""
    @register("setid", False)
    async def set_id_command_handler(self, cmd: ChatCommand):
        if cmd.user.name in self.client.users:
            await cmd.reply("setid")
        else: await cmd.reply("У тебя нет прав на эту команду!")
        
    """!uptime"""
    @register("uptime", False)
    async def uptime_command_handler(self, cmd: ChatCommand):
        if cmd.user.name in self.client.users:
            await cmd.reply(get_uptime(self.start_time))
