
<div align="center">
    <h1>🤡 alaqubot</h1>
    <img height="20" alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11+-blue">
    <img height="20" alt="License Apache 2.0" src="https://img.shields.io/badge/license-MIT-green">
    <img height="20" alt="Status" src="https://img.shields.io/badge/status-pet--project-orange">
    <p><strong>alaqubot</strong> — это twitch-бот для стримера alaqu1337</p>
    <blockquote>(─‿‿─)</blockquote>
</div>

---

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
│   │   ├── cooldown.py     # --- задержка для команд ---
│   │   ├── get_currency.py # --- курс доллара ---
│   │   ├── get_stream.py   # --- получение информации про стрим ---
│   │   ├── fact.py         # --- случайный факт ---
│   │   ├── cards.py        # --- случайная карта ---
│   │   ├── horoscope.py    # --- гороскоп ---
│   │   ├── translate.py    # --- переводчик ---
│   │   ├── weather.py      # --- получение погоды ---
│   │   └── logger.py       # --- логирование ---
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

[src/bot.py](/src/bot.py)
``` python
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat

from .config import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH

from cfg import CLIENT_ID, CLIENT_SECRET, CHANNEL, TOKEN, REFRESH_TOKEN, LOG_PATH
from build import BOOTS, ITEMS
from heroes import HEROES

from utils.logger import LogManager
        
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
            "автор": self.main_commands.author,
            
            "спин": self.fun_commands.spin_command_handler,
            "монетка": self.fun_commands.coin_command_handler,
            "ролл": self.fun_commands.roll_command_handler,
            "удар": self.fun_commands.punch_command_handler,
            "шар": self.fun_commands.ball_command_handler,
            "карты": self.fun_commands.card_command_handler,
            "факт": self.fun_commands.fact_command_handler,
            
            "доллар": self.utility_commands.converter_command_handler,
            "гороскоп": self.utility_commands.horoscope_command_handler,
            "погода": self.utility_commands.weather_command_handler,
            "перевод": self.utility_commands.translate_command_handler,
        }
        
        for name, handler in commands.items():
            self.chat.register_command(name, handler)
```

---

## **🧩 зависимости**
[requirements.txt](/requirements.txt)
```bash
# --- twitch ---
twitchAPI==4.5.0

# --- config ---
environs==14.3.0

# --- logs ---
loguru==0.7.3

# --- web ---
aiohttp==3.12.15
beautifulsoup4==4.13.5

# --- api ---
deep-translator==1.11.4
```

