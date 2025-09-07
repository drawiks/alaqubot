# --- Twitch API import --- #
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

# --- Local import --- #
from .config import (
    CLIENT_ID,
    CLIENT_SECRET,
    CHANNEL,
    TOKEN,
    REFRESH_TOKEN,
    LOG_PATH
)

from .events import MessageEvent, ReadyEvent
from .commands import MainCommands, FunCommands, UtilityCommands
from .utils import LogManager, CurrencyConverter


logger = LogManager(LOG_PATH).logger

# --- Twitch initialization --- #
twitch_session = Twitch(
    app_id=CLIENT_ID,
    app_secret=CLIENT_SECRET
)
twitch_session.set_user_authentication(
    token=TOKEN,
    scope=[
        AuthScope.CHAT_READ,
        AuthScope.CHAT_EDIT
    ],
    refresh_token=REFRESH_TOKEN
)
chat = Chat(twitch=twitch_session)

# --- Event initialization --- #
message_event = MessageEvent(log_path=LOG_PATH)
ready_event = ReadyEvent(log_path=LOG_PATH, channel=CHANNEL)

chat.register_event(event=ChatEvent.MESSAGE, handler=message_event.on_message)
chat.register_event(event=ChatEvent.READY, handler=ready_event.on_ready)

# --- Command initialization --- #
main_commands = MainCommands()
fun_commands = FunCommands()
utility_commands = UtilityCommands(log_path=LOG_PATH)

chat.register_command('команды', main_commands.commands_command_handler)
chat.register_command('тг', main_commands.tg_command_handler)
chat.register_command('гайд', main_commands.guide_command_handler)
chat.register_command('мейн', main_commands.main_command_handler)
chat.register_command('монетка', fun_commands.coin_command_handler)
chat.register_command('ролл', fun_commands.roll_command_handler)
chat.register_command('шар', fun_commands.ball_command_handler)
chat.register_command('доллар', utility_commands.converter_command_handler)
