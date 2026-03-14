from twitchAPI.chat import EventData
from src.utils.logger import logger


async def on_ready(event: EventData, channels: list[str]) -> None:
    logger.info("bot ready")
    for channel in channels:
        await event.chat.join_room(channel)
        logger.info(f"joined {channel}")
