
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN, REFRESH_TOKEN, LOG_PATH

from .events import MessageEvent, ReadyEvent, RaidEvent, FollowEvent, SubscribeEvent
from .commands import MainCommands, FunCommands, UtilityCommands
from .utils import logger, get_commands
        
import asyncio
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        
        self.message_event = MessageEvent()
        self.ready_event = ReadyEvent(CHANNELS)
        
        self.main_commands =  MainCommands()
        self.fun_commands = FunCommands()
        self.utility_commands = UtilityCommands()
    
    async def run(self):
        while True:
            try:
                logger.info("init")
                self.twitch = Twitch(CLIENT_ID, CLIENT_SECRET)
                await self.twitch.set_user_authentication(TOKEN, self.USER_SCOPE, REFRESH_TOKEN)
                        
                self.chat = await Chat(self.twitch)
                self.chat.no_message_reset_time = 5
                
                self.raid_event = RaidEvent(self.chat)
                self.follow_event = FollowEvent(self.chat)
                self.subscribe_event = SubscribeEvent(self.chat)
                
                self.user = await first(self.twitch.get_users(logins=CHANNELS))
                
                self.eventsub = EventSubWebsocket(self.twitch)
                    
                await self.register_events()
                await self.register_commands()
                
                self.chat.start()
                self.eventsub.start()
                
                await self.eventsub.listen_channel_raid(
                    to_broadcaster_user_id=self.user.id, 
                    from_broadcaster_user_id=self.user.id, 
                    callback=self.raid_event.on_raid
                )
                await self.eventsub.listen_channel_follow_v2(
                    broadcaster_user_id=self.user.id, 
                    moderator_user_id=self.user.id, 
                    callback=self.follow_event.on_follow
                )
                await self.eventsub.listen_channel_subscribe(
                    broadcaster_user_id=self.user.id,
                    callback=self.subscribe_event.on_sub
                )
                
                while True:
                    await asyncio.sleep(60)
                
            except Exception as e:
                logger.critical(e)
                logger.info("restart")
            finally:
                if hasattr(self, 'chat'):
                    self.chat.stop()
                if hasattr(self, 'eventsub'):
                    await self.eventsub.stop()
                if hasattr(self, 'twitch'):
                    await self.twitch.close()
            await asyncio.sleep(15)

    async def register_events(self):
        self.chat.register_event(ChatEvent.MESSAGE, self.message_event.on_message)
        self.chat.register_event(ChatEvent.READY, self.ready_event.on_ready)
        self.chat.register_event(ChatEvent.RAID, self.ready_event.on_ready)
    
    async def register_commands(self):
        commands = get_commands()
        for command, (func, owner_name, is_public) in commands.items():
            target = None
            for candidate in (self.main_commands, self.fun_commands, self.utility_commands):
                if candidate.__class__.__name__ == owner_name:
                    target = candidate
                    break

            if target is None:
                target = self.main_commands

            bound = func.__get__(target, target.__class__)
            self.chat.register_command(command, bound)
        