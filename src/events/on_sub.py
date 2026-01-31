
from twitchAPI.object.eventsub import ChannelSubscribeEvent
from twitchAPI.chat import Chat

from src.utils import logger

class SubscribeEvent:
    def __init__(self, chat: Chat):
        self.chat = chat
        
    async def on_sub(self, sub_event: ChannelSubscribeEvent):
        logger.info(f"Новый сабер {sub_event.event.user_name}!")
        
        await self.chat.send_message(sub_event.event.broadcaster_user_name, f"НОВЫЙ САБЕР, {sub_event.event.user_name}!")