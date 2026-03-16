import asyncio
from typing import Callable

from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first

from src.utils.logger import logger


class EventSubManager:
    def __init__(self, twitch, channels: list[str], chat):
        self._twitch = twitch
        self._channels = channels
        self._chat = chat
        self._eventsub: EventSubWebsocket | None = None
        self._callbacks: dict[str, Callable] = {}

    def _create_wrapper(self, event_type: str):
        async def wrapper(event):
            callback = self._callbacks.get(event_type)
            if callback:
                await callback(event, self._chat)

        return wrapper

    def register_callback(self, event_type: str, callback: Callable):
        self._callbacks[event_type] = callback

    async def start(self):
        if not self._twitch:
            logger.warning("EventSub no twitch client")
            return

        self._eventsub = EventSubWebsocket(self._twitch)

        for channel in self._channels:
            user = await first(self._twitch.get_users(logins=channel))
            if not user:
                logger.warning(f"EventSub channel {channel} not found")
                continue

            user_id = user.id

            try:
                await self._eventsub.listen_channel_follow_v2(
                    user_id, user_id, self._create_wrapper("follow")
                )
                await self._eventsub.listen_channel_subscribe(
                    user_id, self._create_wrapper("subscribe")
                )
                await self._eventsub.listen_channel_subscription_gift(
                    user_id, self._create_wrapper("gift")
                )
                await self._eventsub.listen_channel_raid(
                    callback=self._create_wrapper("raid"),
                    to_broadcaster_user_id=user_id,
                )
                await self._eventsub.listen_stream_online(
                    user_id, self._create_wrapper("stream_online")
                )
                await self._eventsub.listen_stream_offline(
                    user_id, self._create_wrapper("stream_offline")
                )
                logger.info(f"EventSub subscribed to events for {channel}")
            except Exception as e:
                logger.error(f"EventSub failed to subscribe to {channel}: {e}")

        try:
            self._eventsub.start()
            logger.info("EventSub started")
        except Exception as e:
            logger.error(f"EventSub failed to start: {e}")

    async def stop(self):
        if self._eventsub:
            await self._eventsub.stop()
            logger.info("EventSub stopped")
