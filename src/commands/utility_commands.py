
from twitchAPI.chat import ChatCommand

from datetime import datetime

from src.utils import (
    CurrencyConverter, 
    Horoscope, Film, 
    get_weather, 
    get_translate, 
    register, 
    cooldown, 
    permission,
    get_uptime
)

class UtilityCommands:
    def __init__(self, log_path):
        self.start_time = datetime.now()
        self.currency_converter = CurrencyConverter(log_path)
        self.horoscope = Horoscope(log_path)
        self.film = Film(log_path)
    
    """!доллар"""
    @register("доллар")
    @cooldown(10)
    async def converter_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply(self.currency_converter.currency(None))
        else:
            await cmd.reply(self.currency_converter.currency(float(cmd.parameter)))
    
    """!гороскоп"""
    @register("гороскоп")
    @cooldown(30)
    async def horoscope_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи свой знак зодиака! (овен, телец, близнецы, рак, лев, дева, весы, скорпион, стрелец, козерог, водолей, рыбы)")
        else:
            result = self.horoscope.fetch(str(cmd.parameter))
            await cmd.reply(result or "Не удалось получить гороскоп для этого знака зодиака.")
            
    """!фильм"""
    @register("фильм")
    @cooldown(30)
    async def film_command_handler(self, cmd: ChatCommand):
        result = self.film.fetch()
        await cmd.reply(result or "Не удалось получить фильм")
    
    """!погода"""
    @register("погода")
    @cooldown(10)
    async def weather_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название города!")
        else:
            await cmd.reply(get_weather(str(cmd.parameter)))
    
    """!перевод"""
    @register("перевод")
    @cooldown(10)
    async def translate_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи текст для перевода!")
        else:
            await cmd.reply(get_translate(str(cmd.parameter)))
    
    """!uptime"""
    @register("uptime")
    @permission()
    async def uptime_command_handler(self, cmd: ChatCommand):
        await cmd.reply(get_uptime(self.start_time))
