
from twitchAPI.chat import ChatMessage
from typing import Any
import time

from src.utils import logger

class MessageEvent:
    def __init__(self, client: Any = None):
        self.client = client
        self._cooldowns = {}
    
    async def on_message(self, msg: ChatMessage):
        logger.trace(f"|room - {msg.room.name if msg.room else ""}| {msg.user.name}: {msg.text}")
        
        now = time.time()
        expired = [u for u, t in self._cooldowns.items() if now - t >= 15]
        for u in expired:
            del self._cooldowns[u]
        
        if "@alaqubot" in msg.text.lower():
            last = self._cooldowns.get(msg.user.name, 0)
            if now - last < 15: return

            self._cooldowns[msg.user.name] = now

            text = msg.text.lower().replace("@alaqubot", "").strip()
            if not text: return

            response = await self.client.post_request("groq", {"text": text})
            await msg.chat.send_message(msg.room.name, f"@{msg.user.name} {response}")