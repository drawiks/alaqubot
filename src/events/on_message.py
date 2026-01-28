
from twitchAPI.chat import ChatMessage

from src.utils import logger

class MessageEvent:
    async def on_message(self, msg: ChatMessage):
        logger.trace(f"|room - {msg.room.name if msg.room else ""}| {msg.user.name}: {msg.text}")