<div align="center">
    <h1>🤡 alaqubot</h1>
    <img height="20" alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11+-blue">
    <img height="20" alt="License Apache 2.0" src="https://img.shields.io/badge/license-MIT-green">
    <img height="20" alt="Status" src="https://img.shields.io/badge/status-release-red">
    <p><strong>alaqubot</strong> — это twitch-бот для стримера alaqu1337</p>
    <blockquote>(─‿‿─)</blockquote>
</div>

---

```
 ______   ___                             ____            __
/\  _  \ /\_ \                           /\  _`\         /\ \__
\ \ \L\ \\//\ \      __       __   __  __\ \ \L\ \    ___\ \ ,_\
 \ \  __ \ \ \ \   /'__`\   /'__`\/\ \/\ \\ \  _ <'  / __`\ \ \/
  \ \ \/\ \ \_\ \_/\ \L\.\_/\ \L\ \ \ \_\ \\ \ \L\ \/\ \L\ \ \ \_
   \ \_\ \_\/\____\ \__/.\_\ \___, \ \____/ \ \____/\ \____/\ \__\
    \/_/\/_/\/____/\/__/\/_/\/___/\ \/___/   \/___/  \/___/  \/__/
                                 \ \_\
                                  \/_/

```

## **📂 структура проекта**

```bash
alaqubot/
│
├── src/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── main_commands.py
│   │   ├── fun_commands.py
│   │   └── utility_commands.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── on_message.py
│   │   └── on_ready.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cooldown.py         # --- задержка для команд ---
│   │   ├── get_currency.py     # --- курс доллара ---
│   │   ├── get_stream.py       # --- получение информации про стрим ---
│   │   ├── fact.py             # --- случайный факт ---
│   │   ├── cards.py            # --- случайная карта ---
│   │   ├── horoscope.py        # --- гороскоп ---
│   │   ├── translate.py        # --- переводчик ---
│   │   ├── weather.py          # --- получение погоды ---
│   │   ├── film.py             # --- рандом фильм ---
│   │   ├── uptime.py           # --- время работы бота ---
│   │   ├── register_command.py # --- регистрация команд ---
│   │   ├── permission.py       # --- права команд ---
│   │   ├── load_commands.py    # --- загрузка команд каналов ---
│   │   ├── cache.py            # --- кеширование ---
│   │   └── logger.py           # --- логирование ---
│   │
│   ├── bot.py
│   ├── config.py
│   └── heroes.py
│
├── alaqubot.py # --- entrypoint ---
│
├── alaqu.jpg
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## **🌐 команды**

```
--- main ---
- !команды
- !тг
- !гайд
- !мейн
- !автор

--- fun ---
- !спин
- !монетка
- !ролл
- !удар
- !шар
- !карты
- !факт
- !зона

--- utility ---
- !доллар
- !гороскоп
- !погода
- !перевод
- !фильм
```

---

[src/bot.py](/src/bot.py)
``` python
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN, REFRESH_TOKEN, LOG_PATH

from .events import MessageEvent, ReadyEvent
from .commands import MainCommands, FunCommands, UtilityCommands
from .utils import LogManager, get_commands
        
import asyncio
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.log = LogManager(LOG_PATH).logger
        
        self.message_event = MessageEvent(LOG_PATH)
        self.ready_event = ReadyEvent(LOG_PATH, CHANNELS)
        
        self.main_commands =  MainCommands()
        self.fun_commands = FunCommands()
        self.utility_commands = UtilityCommands(LOG_PATH)
    
    async def run(self):
        while True:
            try:
                self.log.info("init")
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
                self.log.critical(e)
                self.log.info("restart")
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
```

---

## **🧩 зависимости**
[requirements.txt](/requirements.txt)
```bash
# --- twitch ---
# --- twitch ---
twitchAPI==4.5.0

# --- config ---
environs==14.3.0

# --- database ---
cachetools==6.2.4

# --- logs ---
loguru==0.7.3

# --- web ---
aiohttp==3.12.15
beautifulsoup4==4.13.5

# --- api ---
deep-translator==1.11.4

# --- cli ---
pyfiglet==1.0.4
termcolor==3.3.0
```

