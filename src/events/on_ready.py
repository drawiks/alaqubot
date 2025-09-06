
from twitchAPI.chat import EventData

from src.utils import LogManager

class ReadyEvent:
    def __init__(self, log_path, channel):
        self.log = LogManager(log_path).logger
        self.channel = channel

    async def on_ready(self, ready_event: EventData):
        self.log.info('✅ Бот готов к работе, подключение к каналу')
        await ready_event.chat.join_room(self.channel)