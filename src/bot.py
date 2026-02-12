
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN, REFRESH_TOKEN

from .events import MessageEvent, ReadyEvent
from .utils import logger, get_methods, load_groups
        
import asyncio
import os
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        
        self.message_event = MessageEvent()
        self.ready_event = ReadyEvent(CHANNELS)
        
        
        self.dir = os.path.dirname(__file__)
        self.path = os.path.join(self.dir, "commands")
        self.groups = load_groups(self.path, "src.commands")
    
    async def run(self):
        while True:
            try:
                logger.info("init")
                self.twitch = Twitch(CLIENT_ID, CLIENT_SECRET)
                await self.twitch.set_user_authentication(TOKEN, self.USER_SCOPE, REFRESH_TOKEN)
                        
                self.chat = await Chat(self.twitch)
                self.chat.no_message_reset_time = 5
                    
                await self.register_events()
                await self.register_commands()
                
                self.chat.start()
                
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
    
    async def register_commands(self):
        for group in self.groups:
            group.groups = self.groups
            commands = get_methods(group)
            logger.debug(f"{group} registred")
            for cmd in commands:
                self.chat.register_command(cmd["name"], cmd["func"])