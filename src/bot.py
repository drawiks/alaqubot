from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
import asyncio

from collections import defaultdict
from operator import itemgetter
import random
import time

from utils.logger import LogManager

from cfg import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH
        
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.log = LogManager(LOG_PATH).logger
        self._message_count = defaultdict(int)
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
        self.chat.register_command('мейн', self.main_command_handler)
        self.chat.register_command('топ', self.top_command_handler)
        self.chat.register_command('команды', self.commands_command_handler)
        
        self.chat.register_command('маркиз', self.mrmarkis_command_handler)
        self.chat.register_command('пизденка', self.pizdenka_command_handler)
        
        self.chat.register_command('flip', self.flip_command_handler)
        self.chat.register_command('roll', self.roll_command_handler)
        self.chat.register_command('шар', self.ball_command_handler)

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
        
        self._message_count[msg.user.name] += 1
        
        for cb in self._message_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(msg)
                else:
                    cb(msg)
            except Exception as e:
                self.log.error(f"Ошибка в callback {cb}: {e}")

    def cooldown(seconds=30, per_user=True):
        def wrapper(func):
            async def inner(self, cmd: ChatCommand, *args, **kwargs):
                key = (cmd.user.name, func.__name__) if per_user else func.__name__
                now = time.time()
                
                if not hasattr(self, "_cooldowns"):
                    self._cooldowns = {}

                last_used = self._cooldowns.get(key, 0)
                if now - last_used < seconds:
                    wait = round(seconds - (now - last_used), 1)
                    await cmd.reply(f"Подожди {wait} сек!")
                    return
                
                self._cooldowns[key] = now
                
                return await func(self, cmd, *args, **kwargs)
            return inner
        return wrapper

    @cooldown(10, True)
    async def commands_command_handler(self, cmd: ChatCommand):
        await cmd.reply("!тг, !гайд, !мейн, !маркиз, !flip, !roll, !шар (вопрос)")
    
    @cooldown(30, True)
    async def tg_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("https://t.me/alaquu")
        else:
            if int(cmd.parameter) <= 5:
                for _ in range(int(cmd.parameter)):
                    await cmd.reply("https://t.me/alaquu")
            else:
                await cmd.reply("Дохуя просишь братик) https://t.me/alaquu")
    
    @cooldown(30, True)  
    async def guide_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Гайд на кеза и тинкера - https://t.me/alaquu/460")
    
    @cooldown(30, True)
    async def main_command_handler(self, cmd: ChatCommand):
        await cmd.reply("Мейн егора - https://steamcommunity.com/profiles/76561198993439266")
    
    @cooldown(30, True)
    async def mrmarkis_command_handler(self, cmd: ChatCommand):
        await cmd.reply("https://t.me/+cVieT2VQ3cExNTky")
        
    @cooldown(30, True)
    async def pizdenka_command_handler(self, cmd: ChatCommand):
        await cmd.reply("'А ВОТ БЫЛ БЫ АСПЕКТ ДРУГОЙ СГОРЕЛА БЫ' Похотливая. П 1104 год д.н.эры")
    
    @cooldown(30, True)
    async def flip_command_handler(self, cmd: ChatCommand):
        await cmd.reply(random.choice(["Орёл", "Решка"]))
    
    @cooldown(30, True)
    async def roll_command_handler(self, cmd: ChatCommand):
        await cmd.reply(random.randint(0, 100))
    
    @cooldown(30, True)
    async def ball_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши вопрос!")
        else:
            await cmd.reply(random.choice(["Да", "Нет", "Наверное", "Сомневаюсь", "Точно да", "Точно нет", "Неуверен"]))
    
    @cooldown(60, True)
    async def top_command_handler(self, cmd: ChatCommand):
        if not self._message_count:
            await cmd.reply("Пока никто не писал сообщений")
            return
        
        top_users = sorted(self._message_count.items(), key=itemgetter(1), reverse=True)[:5]
        
        top_text = "Лучшие:\n"
        for _, (user, count) in enumerate(top_users, start=1):
            top_text += f"({_}) {user} — {count}\n"
        
        await cmd.reply(top_text)
        