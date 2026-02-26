<div align="center">
    <h1>🤡 alaqubot</h1>
    <img height="20" alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11+-blue">
    <img height="20" alt="License Apache 2.0" src="https://img.shields.io/badge/license-MIT-green">
    <img height="20" alt="Status" src="https://img.shields.io/badge/status-stable-red">
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
│   ├── api/
│   │   ├── __init__.py
│   │   └── client.py
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
│   │   ├── commands.py         # --- родительский класс команд ---
│   │   ├── cooldown.py         # --- задержка для команд ---
│   │   ├── cache.py            # --- кеширование ---
│   │   ├── discovery.py        # --- динамическая загрузка ---
│   │   ├── uptime.py           # --- время работы бота ---
│   │   ├── register_command.py # --- регистрация команд ---
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
- !ролл
- !шар
- !зона

--- utility ---
- !доллар
- !погода
- !фильм
- !wl
- !mmr
- !setmmr
- !setid
```

---

[src/bot.py](/src/bot.py)
``` python
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN, REFRESH_TOKEN

from .events import MessageEvent, ReadyEvent
from .utils import logger, get_methods, load_groups
from .api import client
        
import asyncio
import os
class Bot:
    def __init__(self):
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        
        self.message_event = MessageEvent(client)
        self.ready_event = ReadyEvent(CHANNELS)
        
        self.dir = os.path.dirname(__file__)
        self.path = os.path.join(self.dir, "commands")
        self.groups = load_groups(self.path, "src.commands", client)
    
    async def run(self):
        while True:
            try:
                logger.info("init")
                await client.load_data()
                
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
                if hasattr(self, 'twitch'):
                    await self.twitch.close()
            await asyncio.sleep(15)

    async def register_events(self):
        self.chat.register_event(ChatEvent.MESSAGE, self.message_event.on_message)
        self.chat.register_event(ChatEvent.READY, self.ready_event.on_ready)
    
    async def register_commands(self):
        for group in self.groups:
            commands = get_methods(group)
            logger.debug(f"{group} registered")
            for cmd in commands:
                self.chat.register_command(cmd["name"], cmd["func"])
```

---

## **🧩 зависимости**
[requirements.txt](/requirements.txt)
```bash
# --- twitch ---
twitchAPI==4.5.0

# --- config ---
environs==14.3.0

# --- data ---
cachetools==6.2.4

# --- logs ---
dlogger-drawiks==0.3.1

# --- web ---
httpx==0.28.1

# --- api ---
deep-translator==1.11.4

# --- cli ---
pyfiglet==1.0.4
dcolor-drawiks==0.2.0
```
