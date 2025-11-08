
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH

from .events import MessageEvent, ReadyEvent
from .commands import MainCommands, FunCommands, UtilityCommands
from .utils import LogManager, get_commands
        
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.log = LogManager(LOG_PATH).logger
        
        self.message_event = MessageEvent(LOG_PATH)
        self.ready_event = ReadyEvent(LOG_PATH, CHANNEL)
        
        self.main_commands =  MainCommands()
        self.fun_commands = FunCommands()
        self.utility_commands = UtilityCommands(LOG_PATH)
    
    async def run(self):
        self.twitch = Twitch(CLIENT_ID, CLIENT_SECRET)
        for _ in range(3):
            await self.twitch.set_user_authentication(TOKEN, self.USER_SCOPE, REFRESH_TOKEN)
                
        self.chat = await Chat(self.twitch)
            
        await self.register_events()
        await self.register_commands()
            
        try:
            self.chat.start()
        except Exception as e:
            self.log.critical(e)
        finally:
            await self.twitch.close()

    async def register_events(self):
        self.chat.register_event(ChatEvent.MESSAGE, self.message_event.on_message)
        self.chat.register_event(ChatEvent.READY, self.ready_event.on_ready)
    
    async def register_commands(self):
        commands = get_commands()
        for cmd_name, (func, owner_name) in commands.items():
            target = None
            for candidate in (self.main_commands, self.fun_commands, self.utility_commands):
                if candidate.__class__.__name__ == owner_name:
                    target = candidate
                    break

            if target is None:
                target = self.main_commands

            bound = func.__get__(target, target.__class__)
            self.chat.register_command(cmd_name, bound)
        