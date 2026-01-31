
from twitchAPI.chat import ChatMessage

from src.utils import logger
from src.api import client

class MessageEvent:
    async def on_message(self, msg: ChatMessage):
        logger.trace(f"|room - {msg.room.name if msg.room else ""}| {msg.user.name}: {msg.text}")
        if f"@{self.bot_nick}" in msg.text.lower():
            text = msg.text.lower().replace(f"@{self.bot_nick}", "").strip()
            
            response = await client.post_request("groq", {"text":text})
            
            await msg.chat.send_message(msg.room.name, f"@{msg.user.name} {response}")