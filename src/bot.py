from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand

from collections import defaultdict
import asyncio, aiohttp, random, time, re

from g4f.client import Client, AsyncClient
from translate import Translator

from cfg import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH
from build import BOOTS, ITEMS
from heroes import HEROES

from utils.logger import LogManager
        
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
        self.chat.register_command('герой', self.hero_command_handler)
        self.chat.register_command('билд', self.build_command_handler)
        self.chat.register_command('мейн', self.main_command_handler)
        self.chat.register_command('команды', self.commands_command_handler)
        
        self.chat.register_command('гпт', self.gpt_command_handler)
        self.chat.register_command('арт', self.art_command_handler)
        self.chat.register_command('перевод', self.translate_command_handler)
        
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
        
        #any(word in text.lower() for word in ["@alaqubot", "алакубот"]) не трогать я потратил минут 20 на это
        text = msg.text.strip()
        if any(word in text.lower() for word in ["@alaqubot", "алакубот"]):
            text = msg.text.split()
            text = [w for w in text if w.lower() not in ["@alaqubot", "алакубот"]]
            text = "".join(text)
            
            for _ in self.split_message(await self.generate_text(text)):
                    await msg.reply(_)
                    await asyncio.sleep(0.4)
        
        elif msg.reply_parent_user_login:
            if msg.reply_parent_user_login.lower() == "alaqubot":
                text = msg.text.split()
                if "@alaqubot" in text:
                    text.remove("@alaqubot")
                text = "".join(text)
                
                for _ in self.split_message(await self.generate_text(text)):
                    await msg.reply(_)
                    await asyncio.sleep(0.4)
                
        
        for cb in self._message_callbacks:
            try:    
                if asyncio.iscoroutinefunction(cb):
                    await cb(msg)
                else:
                    cb(msg)
            except Exception as e:
                self.log.error(f"Ошибка в callback {cb}: {e}")

    async def send_message(self, text):
        await self.chat.send_message(CHANNEL, text)
    
    def split_message(self, text: str, limit: int = 500, max_parts: int = 2) -> list[str]:
        parts = []
        while len(text) > limit and len(parts) < max_parts - 1:
            split_at = text.rfind(" ", 0, limit)
            if split_at == -1:
                split_at = limit
            parts.append(text[:split_at].strip())
            text = text[split_at:].strip()
        if text:
            if len(text) > limit:
                text = text[:limit - 3] + "..."
            parts.append(text)

        return parts

    async def generate_text(self, prompt: str):
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4.1",  # Try "gpt-4.1", "gpt-4o", "deepseek-v3", etc.
            messages=[{"role": "user", "content": prompt}],
            web_search=True
        )
        text = response.choices[0].message.content
        text = re.sub(r'(\*\*|\*|`|\#\#\#)', '', text)
        
        return text
    
    async def shorten_url(self, url: str) -> str:
        api = f"http://tinyurl.com/api-create.php?url={url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as response:
                return await response.text()
    
    async def generate_art(self, prompt: str):
        client = AsyncClient()
        response = await client.images.generate(
            prompt=prompt,
            model="flux",
            response_format="url"
        )
        
        return await self.shorten_url(response.data[0].url)
    
    async def translate(self, text: str, lang: str):
        translated = Translator(to_lang=lang, from_lang="ru").translate(text)
        if len(translated) > 500:
            translated = translated[:497] + "..."
        return translated
    
    def cooldown(seconds=30, per_user=True):
        ignore_users = ["drawksr69", "alaqu1337"]
        def wrapper(func):
            async def inner(self, cmd: ChatCommand, *args, **kwargs):
                if cmd.user.name in ignore_users:
                    return await func(self, cmd, *args, **kwargs)
                
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
        await cmd.reply("!тг, !гайд, !герой, !билд, !мейн, !гпт (запрос), !арт (запрос), !flip, !roll, !шар (вопрос)")
    
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
        await cmd.reply("Мейн Егора - https://steamcommunity.com/profiles/76561198993439266")
    
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
            await cmd.reply(
                random.choice(["Да", "Нет", "Точно да", "Точно нет", "Неуверен", "Наверное", "Не сейчас", "Спроси снова"]))
            
            
    @cooldown(30, True)
    async def hero_command_handler(self, cmd: ChatCommand):
        await cmd.reply(f"Тебе выпал: {random.choice(HEROES)}")
        
    @cooldown(30, True)
    async def build_command_handler(self, cmd: ChatCommand):
        boots = random.choice(BOOTS)
        items = random.sample(ITEMS, 5)
        build = [boots] + items
        await cmd.reply("Твой билд: " + ", ".join(build))
        
    @cooldown(45, True)
    async def gpt_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши запрос!")
        else:
            text = await self.generate_text(cmd.parameter)
            for _ in self.split_message(text):
                await cmd.reply(_)
                await asyncio.sleep(0.4)
                
    @cooldown(45, True)
    async def art_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши запрос!")
        else:
            await cmd.reply(await self.generate_art(cmd.parameter))
            
    @cooldown(20, True)
    async def translate_command_handler(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("Напиши текст для перевода!")
        else:
            await cmd.reply(await self.translate(cmd.parameter, "ru"))