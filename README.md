
<div align="center">
    <h1>🤡 alaqubot v1.3.0</h1>
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
│   ├── assets/
│   │   ├── fonts/
│   │   │   ├── IBMPlexSans-Bold.ttf
│   │   │   ├── IBMPlexSans-Medium.ttf
│   │   │   ├── Jersey20-Regular.ttf
│   │   │   └── NotoSans-Regular.ttf
│   │   └── icon.ico
│   ├── utils/
│   │   └── logger.py # --- логирование ---
│   │
│   ├── app.py # --- entrypoint ---
│   ├── bot.py
│   ├── config.py
│   ├── build.py
│   └── heroes.py
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

# --- ui ---
flet==0.28.3

# --- web ---
aiohttp==3.12.15

# --- api ---
g4f==0.6.1.6
translate==3.6.1
```

