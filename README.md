
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
translate==3.6.1
```

