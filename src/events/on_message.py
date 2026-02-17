
from twitchAPI.chat import ChatMessage
from typing import Any

from src.utils import logger

class MessageEvent:
    def __init__(self, client: Any = None):
        self.client = client
    
    async def on_message(self, msg: ChatMessage):
        logger.trace(f"|room - {msg.room.name if msg.room else ""}| {msg.user.name}: {msg.text}")
        if "@alaqubot" in msg.text.lower():
            text = msg.text.lower().replace("@alaqubot", "").strip()
            
            response = await self.client.post_request("groq", {"text":text})
            
            await msg.chat.send_message(msg.room.name, f"@{msg.user.name} {response}")