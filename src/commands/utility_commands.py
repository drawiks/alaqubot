
from twitchAPI.chat import ChatCommand

from src.utils import CurrencyConverter, Horoscope, get_weather, get_translate, register

class UtilityCommands:
    def __init__(self, log_path):
        self.currency_converter = CurrencyConverter(log_path)
        self.horoscope = Horoscope(log_path)
    
    """!доллар"""
    @register("доллар")
    async def converter_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply(self.currency_converter.currency(None))
        else:
            await cmd.reply(self.currency_converter.currency(float(cmd.parameter)))
    
    """!гороскоп"""
    @register("гороскоп")
    async def horoscope_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи свой знак зодиака! (овен, телец, близнецы, рак, лев, дева, весы, скорпион, стрелец, козерог, водолей, рыбы)")
        else:
            await cmd.reply(self.horoscope.fetch(str(cmd.parameter)))
    
    """!погода"""
    @register("погода")
    async def weather_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи название города!")
        else:
            await cmd.reply(get_weather(str(cmd.parameter)))
    
    """!перевод"""
    @register("перевод")
    async def translate_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи текст для перевода!")
        else:
            await cmd.reply(get_translate(str(cmd.parameter)))
