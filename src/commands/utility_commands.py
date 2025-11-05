
from twitchAPI.chat import ChatCommand

from src.utils import CurrencyConverter, Horoscope

class UtilityCommands:
    def __init__(self, log_path):
        self.currency_converter = CurrencyConverter(log_path)
        self.horoscope = Horoscope(log_path)
        
    async def converter_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply(self.currency_converter.currency(None))
        else:
            await cmd.reply(self.currency_converter.currency(float(cmd.parameter)))
    
    async def horoscope_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Введи свой знак зодиака! (овен, телец, близнецы, рак, лев, дева, весы, скорпион, стрелец, козерог, водолей, рыбы)")
        else:
            await cmd.reply(self.horoscope.fetch(str(cmd.parameter)))