
from twitchAPI.chat import ChatMessage

from src.utils import LogManager

class MessageEvent:
    def __init__(self, log_path):
        self.log = LogManager(log_path).logger

    async def on_message(self, msg: ChatMessage):
        self.log.trace(f"{msg.user.name}: {msg.text}")