from twitchAPI.object.eventsub import ChannelFollowEvent

from src.utils.logger import logger


async def on_follow(event: ChannelFollowEvent, chat) -> None:
    message = f"Новый фолловер, {event.event.user_name}!"
    await chat.send_message(event.event.broadcaster_user_name, message)
    logger.info(f"EventSub new follow from {event.event.user_name}")
