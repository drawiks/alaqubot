
from twitchAPI.object.eventsub import ChannelFollowEvent
from twitchAPI.chat import Chat

from src.utils import logger

class FollowEvent:
    def __init__(self, chat: Chat):
        self.chat = chat
        
    async def on_follow(self, follow_event: ChannelFollowEvent):
        logger.info(f"Новый фолловер {follow_event.event.user_name}!")
        
        await self.chat.send_message(follow_event.event.broadcaster_user_name, f"НОВЫЙ ФОЛЛОВЕР, {follow_event.event.user_name}!")