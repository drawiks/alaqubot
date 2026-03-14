from typing import Any
from src.utils.logger import logger


class ReadyEvent:
    def __init__(self, channels: list[str]) -> None:
        self._channels = channels

    async def on_ready(self, bot: Any, chatbot: Any) -> None:
        logger.info(f"bot ready")
        for channel in self._channels:
            await chatbot.join_room(channel)
            logger.info(f"joined {channel}")
