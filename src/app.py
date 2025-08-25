from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
import asyncio

from utils.logger import LogManager

from config import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH
        
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.logger = LogManager(LOG_PATH)
        
    async def run(self):
        twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
        await twitch.set_user_authentication(TOKEN, self.USER_SCOPE, REFRESH_TOKEN)

        chat = await Chat(twitch)

        chat.register_event(ChatEvent.READY, self.on_ready)
        chat.register_event(ChatEvent.MESSAGE, self.on_message)

        chat.register_command('тг', self.tg_command_handler)
        chat.register_command('гайд', self.guide_command_handler)

        chat.start()

        try:
            input('Нажмите ENTER для остановки работы\n')
        finally:
            chat.stop()
            await twitch.close()
            
    async def on_ready(self, ready_event: EventData):
        print('✅Бот готов к работе, подключение к каналу')
        await ready_event.chat.join_room(CHANNEL)

    async def on_message(self, msg: ChatMessage):
        print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')

    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("https://t.me/alaquu")
        else:
            for _ in range(int(cmd.parameter)):
                await cmd.reply("https://t.me/alaquu")
        
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply(f"Гайд на кеза и тинкера - https://t.me/alaquu/460")

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())