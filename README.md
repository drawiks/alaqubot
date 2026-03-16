<div align="center">
    <h1>🤡 alaqubot</h1>
    <img height="20" alt="Python 3.14+" src="https://img.shields.io/badge/python-3.14+-blue">
    <img height="20" alt="License GPL v3" src="https://img.shields.io/badge/license-GPLv3-green">
    <img height="20" alt="Status" src="https://img.shields.io/badge/status-beta-red">
    <a href="https://github.com/Teekeks/pyTwitchAPI">
      <img height="20" alt="Framework" src="https://img.shields.io/badge/framework-twitchAPI-orange">
    </a>
    <p>Twitch бот для стримера <strong>alaqu1337</strong></p>
    <blockquote>(─‿‿─)</blockquote>
</div>

---

## 🚀 Quick Start

### Клонирование и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/drawiks/alaqubot.git
cd alaqubot

# Скопировать пример .env
cp .env.example .env

# Отредактировать .env
nano .env

# Запустить
python alaqubot.py
```

### Docker

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

---

## ✨ Возможности

| Возможность | Описание |
|------------|----------|
| 🧩 Плагинная архитектура | Добавляй новые функции без изменения ядра |
| 🔍 Авто-обнаружение | Плагины загружаются автоматически |
| ⚙️ YAML конфигурация | Настраивай плагины через YAML файлы |
| 🐳 Docker ready | Запусти в контейнере за минуту |
| 🔄 Auto restart | Бот автоматически перезагружается при ошибках |
| ⏱️ Rate limiting | Встроенная защита от спама |
| 📝 Логирование | Ротация логов, сжатие, retention |
| 🔔 EventSub | Уведомления о follow, subscribe, raid, stream |

---

## 📋 Команды

### Основные

| Команда | Описание                     |
|---------|------------------------------|
| `!команды` | Список всех доступных команд |
| `!тг` | Ссылка на Telegram канал     |
| `!автор` | Авторы проекта               |
| `!гайд` | Гайд на героя                |
| `!мейн` | Основной аккаунт             |

### Развлечения

| Команда | Описание              |
|---------|-----------------------|
| `!спин` | Слоты                 |
| `!ролл` | Случайное число 0-100 |
| `!зона` | Случайная зона        |
| `!шар` | Волшебный шар         |

### Утилиты

| Команда | Описание                         |
|---------|----------------------------------|
| `!доллар` | Курс доллара                     |
| `!погода <город>` | Погода в городе                  |
| `!фильм` | Случайный фильм                  |
| `!wl` | Winrate последних матчей         |
| `!mmr` | Текущий MMR                      |
| `!setmmr` | Установить MMR (для модеров)     |
| `!setid` | Установить Dota ID (для модеров) |
| `!uptime` | Время работы бота (для модеров)  |

---

## 🏗️ Архитектура

```
alaqubot/
├── .env                        # Переменные окружения
├── .env.example                # Пример конфигурации
├── src/
│   ├── bot.py                  # Orchestrator - управление жизненным циклом
│   ├── config.py               # Загрузка конфигов
│   ├── core/
│   │   └── plugin.py           # Базовый класс Plugin
│   ├── plugins/                # Плагины (включая конфиги)
│   │   ├── fun/
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py
│   │   │   └── config.yaml
│   │   ├── main/
│   │   └── utility/
│   ├── handlers/               # Обработчики событий
│   │   ├── events/            # Chat события (message, ready)
│   │   └── eventsub/         # EventSub события (follow, subscribe, raid, stream)
│   ├── services/              # Бизнес-логика
│   │   ├── plugin_manager.py  # Управление плагинами
│   │   ├── auth.py           # Аутентификация
│   │   └── cooldown.py       # Кулдаун команд
│   ├── adapters/             # API клиенты
│   │   ├── api/
│   │   └── twitch/
│   └── utils/                # Утилиты
├── alaqubot.py                # Точка входа
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### Как работает система плагинов

1. Бот сканирует директорию `src/plugins/`
2. Для каждой директории загружается `plugin.py` с классом `XxxPlugin`
3. Конфигурация читается из `src/plugins/xxx/config.yaml`
4. Команды регистрируются автоматически
5. При перезагрузке плагины выгружаются и загружаются заново

### EventSub события

Бот подписывается на события Twitch через WebSocket:

| Событие | Описание |
|---------|----------|
| `channel.follow` | Новый фолловер |
| `channel.subscribe` | Новая подписка |
| `channel.subscription.gift` | Подаренная подписка |
| `channel.raid` | Рейд на канал |
| `stream.online` | Стрим начался |
| `stream.offline` | Стрим закончился |

---

## 🐳 Docker

### Сборка

```bash
docker-compose build
```

### Запуск в фоновом режиме

```bash
docker-compose up -d
```

### Просмотр логов

```bash
docker-compose logs -f bot
```

### Пересборка

```bash
docker-compose up --build -d
```

### Остановка

```bash
docker-compose down
```

---

## ⚙️ Конфигурация

### .env переменные

| Переменная | Описание | Пример |
|-----------|----------|--------|
| `CLIENT_ID` | Twitch Client ID | `abc123...` |
| `CLIENT_SECRET` | Twitch Client Secret | `secret...` |
| `TOKEN` | Twitch Access Token | `oauth:...` |
| `REFRESH_TOKEN` | Twitch Refresh Token | `oauth:...` |
| `CHANNELS` | Каналы через запятую | `alaqu1337,channel2` |
| `LOG_PATH` | Путь к логам | `logs/bot.log` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `LOG_ROTATION` | Ротация логов | `10MB` |
| `LOG_RETENTION` | Хранение логов | `7 days` |

### Конфиги плагинов

Каждый плагин имеет свой YAML конфиг в `src/plugins/<plugin_name>/config.yaml`:

```yaml
enabled: true

commands:
  команда:
    cooldown: 10       # Кулдаун в секундах
    enabled: true
    requires_permission: false

settings:
  # Специфичные настройки плагина
  words:
    - "слово1"
    - "слово2"
```

---

## 🛠️ Разработка плагинов

Подробная документация доступна в [Wiki](https://github.com/drawiks/alaqubot/wiki):

- [Быстрый старт](https://github.com/drawiks/alaqubot/wiki/Быстрый-старт)
- [Структура плагина](https://github.com/drawiks/alaqubot/wiki/Структура-плагина)
- [Конфигурация](https://github.com/drawiks/alaqubot/wiki/Конфигурация)
- [Plugin API](https://github.com/drawiks/alaqubot/wiki/Plugin-API)
- [Примеры](https://github.com/drawiks/alaqubot/wiki/Примеры)
- [Распространение](https://github.com/drawiks/alaqubot/wiki/Распространение)

---

## 📦 Зависимости

```
twitchAPI==4.5.0        # Twitch API
environs==14.6.0        # Конфигурация
pyyaml==6.0.3           # YAML парсинг
httpx==0.28.1           # HTTP клиент
dlogger-drawiks==0.3.8  # Логирование
pyfiglet==1.0.4         # ASCII арт
dcolor-drawiks==0.2.0   # Цветной вывод
```

---

## 📄 License

GNU General Public License v3 - см. [LICENSE](LICENSE)

---

## 👤 Авторы

- [drawiks](https://github.com/drawiks) - Основная разработка

---

<div align="center">
    <p>Сделано с ❤️ для alaqu1337</p>
    <p>(─‿‿─)</p>
</div>
