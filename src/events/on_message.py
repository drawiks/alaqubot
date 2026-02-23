
from twitchAPI.chat import ChatMessage
from typing import Any
import time

from src.utils import logger

class MessageEvent:
    GLOBAL_RATE_LIMIT = 30
    USER_COOLDOWN = 15
    
    def __init__(self, client: Any = None):
        self.client = client
        self._user_cooldowns = {}
        self._global_requests = []
    
    def _check_global_limit(self) -> bool:
        now = time.time()
        self._global_requests = [t for t in self._global_requests if now - t < 60]
        
        if len(self._global_requests) >= self.GLOBAL_RATE_LIMIT:
            return False
        
        self._global_requests.append(now)
        return True
    
    async def on_message(self, msg: ChatMessage):
        logger.trace(f"|room - {msg.room.name if msg.room else ""}| {msg.user.name}: {msg.text}")
        
        now = time.time()
        expired = [u for u, t in self._user_cooldowns.items() if now - t >= self.USER_COOLDOWN]
        for u in expired:
            del self._user_cooldowns[u]
        
        if "@alaqubot" in msg.text.lower():
            last = self._user_cooldowns.get(msg.user.name, 0)
            if now - last < self.USER_COOLDOWN: return

            if not self._check_global_limit():
                await msg.reply("Слишком много запросов, попробуй позже")
                return

            self._user_cooldowns[msg.user.name] = now

            text = msg.text.lower().replace("@alaqubot", "").strip()
            if not text: return

            response = await self.client.post_request("groq", {"text": text})
            await msg.chat.send_message(msg.room.name, f"@{msg.user.name} {response}")