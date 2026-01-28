
from twitchAPI.chat import EventData

from src.utils import logger

class ReadyEvent:
    def __init__(self, channel):
        self.channel = channel

    async def on_ready(self, ready_event: EventData):
        logger.info('✅ Бот готов к работе, подключение к каналу')
        await ready_event.chat.join_room(self.channel)