from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
import asyncio

from utils.logger import LogManager

from cfg import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH
        
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.log = LogManager(LOG_PATH).logger
        self._message_callbacks = []
        self._ready_callbacks = []
        
    def add_message_callback(self, callback):
        self._message_callbacks.append(callback)
        
    def add_ready_callback(self, callback):
        self._ready_callbacks.append(callback)
    
    async def get_stream(self):
        async for user in self.twitch.get_users(logins=[CHANNEL]):
            user_id = user.id
            found = False
            async for stream in self.twitch.get_streams(user_id=[user_id]):
                data = {
                    "status":"online",
                    "title":stream.title,
                    "viewer_count":stream.viewer_count,
                    "game_name":stream.game_name
                }
                
                found = True
                return data
                
            if not found:
                return "❌ Стрим оффлайн"
    
    async def run(self):
        self.twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
        
        for _ in range(3):
            await self.twitch.set_user_authentication(TOKEN, self.USER_SCOPE, REFRESH_TOKEN)

        self.chat = await Chat(self.twitch)

        self.chat.register_event(ChatEvent.READY, self.on_ready)
        self.chat.register_event(ChatEvent.MESSAGE, self.on_message)

        self.chat.register_command('тг', self.tg_command_handler)
        self.chat.register_command('гайд', self.guide_command_handler)
        
        self.chat.register_command('test', self.test_handler)

        self.chat.start()
        
    async def stop(self):
        if self.chat:
            self.chat.stop()
            self.chat = None
        if self.twitch:
            await self.twitch.close()
            self.twitch = None
        self.log.info("❌ Бот остановлен")
            
    async def on_ready(self, ready_event: EventData):
        self.log.info('✅ Бот готов к работе, подключение к каналу')
        await ready_event.chat.join_room(CHANNEL)
        
        for cb in self._ready_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb()
                else:
                    cb()
            except Exception as e:
                self.log.error(f"Ошибка в ready-callback {cb}: {e}")

    async def on_message(self, msg: ChatMessage):
        self.log.debug(f"in {msg.room.name}, {msg.user.name} said: {msg.text}")
        
        for cb in self._message_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(msg)
                else:
                    cb(msg)
            except Exception as e:
                self.log.error(f"Ошибка в callback {cb}: {e}")

    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("https://t.me/alaquu")
        else:
            if int(cmd.parameter) <= 5:
                for _ in range(int(cmd.parameter)):
                    await cmd.reply("https://t.me/alaquu")
            else:
                await cmd.reply("дохуя просишь братик) https://t.me/alaquu")
        
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply(f"Гайд на кеза и тинкера - https://t.me/alaquu/460")
        
    async def test_handler(self, cmd: ChatCommand):
        info = await self.get_stream()
        if type(info) == dict:
            await cmd.reply(info)
        else:
            await cmd.reply(info)
        
