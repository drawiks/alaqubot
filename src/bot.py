
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN, REFRESH_TOKEN, LOG_PATH

from .events import MessageEvent, ReadyEvent
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
                await self.twitch.close()
            await asyncio.sleep(15)

    async def register_events(self):
        self.chat.register_event(ChatEvent.MESSAGE, self.message_event.on_message)
        self.chat.register_event(ChatEvent.READY, self.ready_event.on_ready)
    
    async def register_commands(self):
        commands = get_commands()
        for cmd_name, (func, owner_name, is_public) in commands.items():
            target = None
            for candidate in (self.main_commands, self.fun_commands, self.utility_commands):
                if candidate.__class__.__name__ == owner_name:
                    target = candidate
                    break

            if target is None:
                target = self.main_commands

            bound = func.__get__(target, target.__class__)
            self.chat.register_command(cmd_name, bound)
        