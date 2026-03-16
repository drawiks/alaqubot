from twitchAPI.object.eventsub import ChannelSubscriptionGiftEvent

from src.utils.logger import logger


async def on_gift(event: ChannelSubscriptionGiftEvent, chat) -> None:
    message = f"Спасибо за {event.event.total} подписок, {event.event.user_name}!"
    await chat.send_message(event.event.broadcaster_user_name, message)
    logger.info(
        f"EventSub gift sub from {event.event.user_name}, {event.event.total} subs"
    )
