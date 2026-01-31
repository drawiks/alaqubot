
from twitchAPI.object.eventsub import ChannelRaidEvent
from twitchAPI.chat import Chat

from src.utils import logger

class RaidEvent:
    def __init__(self, chat: Chat):
        self.chat = chat
    
    async def on_raid(self, raid_event: ChannelRaidEvent):
        logger.info(f"Новый рейд от {raid_event.event.from_broadcaster_user_name} с {raid_event.event.viewers} зрителями!")
        
        await self.chat.send_message(raid_event.event.to_broadcaster_user_name, f"Спасибо за рейд, {raid_event.event.from_broadcaster_user_name}!")