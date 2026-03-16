from twitchAPI.object.eventsub import StreamOnlineEvent, StreamOfflineEvent

from src.utils.logger import logger


async def on_stream_online(event: StreamOnlineEvent, chat) -> None:
    message = f"Стрим начался! Время начала: {event.event.started_at}"
    await chat.send_message(event.event.broadcaster_user_name, message)
    logger.info(f"EventSub stream online - {event.event.broadcaster_user_name}")


async def on_stream_offline(event: StreamOfflineEvent, chat) -> None:
    logger.info(f"EventSub stream offline - {event.event.broadcaster_user_name}")
