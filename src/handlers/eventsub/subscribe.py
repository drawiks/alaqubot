from twitchAPI.object.eventsub import ChannelSubscribeEvent

from src.utils.logger import logger


async def on_subscribe(event: ChannelSubscribeEvent, chat) -> None:
    message = f"Спасибо за подписку, {event.event.user_name}!"
    await chat.send_message(event.event.broadcaster_user_name, message)
    logger.info(f"EventSub new sub from {event.event.user_name}")
