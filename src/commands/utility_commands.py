
from twitchAPI.chat import ChatCommand

from datetime import datetime

from src.utils import (
    register, 
    cooldown, 
    permission,
    get_uptime
)

from src.api import client

class UtilityCommands:
    def __init__(self):
        self.start_time = datetime.now()

    """!доллар"""
    @register("доллар")
    @cooldown(10)
    async def converter_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            result = await client.request("currency")
            await cmd.reply(result)
        else:
            result = await client.request("currency", float(cmd.parameter))
            await cmd.reply(result)
            
    """!гороскоп"""
    @register("гороскоп")
    @cooldown(30)
    async def horoscope_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи свой знак зодиака! (овен, телец, близнецы, рак, лев, дева, весы, скорпион, стрелец, козерог, водолей, рыбы)")
        else:
            result = await client.request("horoscope", str(cmd.parameter))
            await cmd.reply(result)
    
    """!вики"""
    @register("вики")
    @cooldown(30)
    async def wiki_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название статьи!")
        else:
            result = await client.request("wiki", str(cmd.parameter))
            await cmd.reply(result)
            
    """!фильм"""
    @register("фильм")
    @cooldown(30)
    async def film_command_handler(self, cmd: ChatCommand):
        result = await client.request("film")
        await cmd.reply(result)
        
    """!майнкрафт"""
    @register("майнкрафт")
    @cooldown(30)
    async def minecraft_command_handler(self, cmd: ChatCommand):
        result = await client.request("minecraft")
        await cmd.reply(result)
    
    """!погода"""
    @register("погода")
    @cooldown(10)
    async def weather_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название города!")
        else:
            result = await client.request("weather", str(cmd.parameter))
            await cmd.reply(result)
    
    """!перевод"""
    @register("перевод")
    @cooldown(10)
    async def translate_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи текст для перевода!")
        else:
            result = await client.request("translate", str(cmd.parameter))
            await cmd.reply(result)
    
    """!uptime"""
    @register("uptime")
    @permission(client.users)
    async def uptime_command_handler(self, cmd: ChatCommand):
        await cmd.reply(get_uptime(self.start_time))
