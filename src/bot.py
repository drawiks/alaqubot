
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH

from .events import MessageEvent, ReadyEvent
from .commands import MainCommands, FunCommands, UtilityCommands
from .utils import LogManager
        
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
        commands = {
            "команды": self.main_commands.commands_command_handler,
            "тг": self.main_commands.tg_command_handler,
            "гайд": self.main_commands.guide_command_handler,
            "мейн": self.main_commands.main_command_handler,
            
            "спин": self.fun_commands.spin_command_handler,
            "монетка": self.fun_commands.coin_command_handler,
            "ролл": self.fun_commands.roll_command_handler,
            "удар": self.fun_commands.punch_command_handler,
            "шар": self.fun_commands.ball_command_handler,
            "школьницы": self.fun_commands.schoolgirl,
            
            "доллар": self.utility_commands.converter_command_handler
        }
        
        for name, handler in commands.items():
            self.chat.register_command(name, handler)
        