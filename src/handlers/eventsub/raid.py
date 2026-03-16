from twitchAPI.object.eventsub import ChannelRaidEvent

from src.utils.logger import logger


async def on_raid(event: ChannelRaidEvent, chat) -> None:
    message = f"{event.event.from_broadcaster_user_name} рейдит {event.event.viewers} с зрителями!"
    await chat.send_message(event.event.to_broadcaster_user_name, message)
    logger.info(
        f"EventSub raid from {event.event.from_broadcaster_user_name} with {event.event.viewers} viewers"
    )
