from twitchAPI.chat import ChatMessage
from typing import TYPE_CHECKING, Optional
import time

from src.utils.logger import logger

if TYPE_CHECKING:
    from src.adapters.api.client import APIClient


GLOBAL_RATE_LIMIT = 30
USER_COOLDOWN = 15

_user_cooldowns: dict[str, float] = {}
_global_requests: list[float] = []


def _check_global_limit() -> bool:
    global _global_requests
    now = time.time()
    _global_requests = [t for t in _global_requests if now - t < 60]

    if len(_global_requests) >= GLOBAL_RATE_LIMIT:
        return False

    _global_requests.append(now)
    return True


async def on_message(msg: ChatMessage, client: Optional["APIClient"]) -> None:
    global _user_cooldowns
    
    logger.trace(
        f"|room - {msg.room.name if msg.room else ''}| {msg.user.name}: {msg.text}"
    )

    now = time.time()
    expired = [
        u for u, t in _user_cooldowns.items() if now - t >= USER_COOLDOWN
    ]
    for u in expired:
        del _user_cooldowns[u]

    if "@alaqubot" in msg.text.lower():
        last = _user_cooldowns.get(msg.user.name, 0)
        if now - last < USER_COOLDOWN:
            return

        if not _check_global_limit():
            await msg.reply("Слишком много запросов, попробуй позже")
            return

        _user_cooldowns[msg.user.name] = now

        text = msg.text.lower().replace("@alaqubot", "").strip()
        if not text:
            return

        response = await client.post_request("groq", {"text": text})  # type: ignore[union-attr]
        if msg.room:
            await msg.chat.send_message(msg.room.name, f"@{msg.user.name} {response}")  # type: ignore[union-attr]


def cleanup() -> None:
    global _user_cooldowns, _global_requests
    _user_cooldowns.clear()
    _global_requests.clear()
