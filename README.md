<div align="center">
    <h1>🤡 AlaquBot</h1>
    <img height="20" alt="Python 3.14+" src="https://img.shields.io/badge/python-3.14+-blue">
    <img height="20" alt="License MIT" src="https://img.shields.io/badge/license-MIT-green">
    <img height="20" alt="Docker" src="https://img.shields.io/badge/docker-ready-blue">
    <p>Twitch бот с плагинной архитектурой для стримера <strong>alaqu1337</strong></p>
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
python main.py
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

---

## 📋 Команды

### Основные

| Команда | Описание |
|---------|----------|
| `!команды` | Список всех доступных команд |
| `!тг` | Ссылка на Telegram канал |
| `!автор` | Авторы проекта |
| `!гайд` | Гайд по боту |
| `!мейн` | Основной канал |

### Развлечения

| Команда | Описание |
|---------|----------|
| `!спин` | Игра в слоты |
| `!ролл` | Случайное число 0-100 |
| `!зона` | Случайная зона |
| `!шар` | Волшебный шар |

### Утилиты

| Команда | Описание |
|---------|----------|
| `!доллар` | Курс доллара |
| `!погода <город>` | Погода в городе |
| `!фильм` | Случайный фильм |
| `!wl` | Winrate последних матчей |
| `!mmr` | Текущий MMR |
| `!setmmr` | Установить MMR (для модеров) |
| `!setid` | Установить Dota ID (для модеров) |
| `!uptime` | Время работы бота |

---

## 🏗️ Архитектура

```
alaqubot/
├── .env                      # Переменные окружения
├── .env.example              # Пример конфигурации
├── src/
│   ├── bot.py              # Ядро бота
│   ├── config.py           # Загрузка конфигов
│   ├── core/
│   │   └── plugin.py      # Базовый класс Plugin
│   ├── plugins/            # Плагины (включая конфиги)
│   │   ├── fun/
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py
│   │   │   └── config.yaml
│   │   ├── main/
│   │   └── utility/
│   ├── events/            # Обработчики событий
│   ├── adapters/          # API клиенты
│   └── utils/             # Утилиты
├── main.py                # Точка входа
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
| `RATE_LIMIT_GLOBAL` | Глобальный лимит | `30` |
| `RATE_LIMIT_USER` | Лимит на пользователя | `15` |

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
pyyaml==6.0.2           # YAML парсинг
httpx==0.28.1           # HTTP клиент
dlogger-drawiks==0.3.8  # Логирование
pyfiglet==1.0.4         # ASCII арт
dcolor-drawiks==0.2.0   # Цветной вывод
```

---

## 📄 License

MIT License - см. [LICENSE](LICENSE)

---

## 👤 Авторы

- [drawiks](https://github.com/drawiks) - Основная разработка

---

<div align="center">
    <p>Сделано с ❤️ для alaqu1337</p>
    <p>(─‿‿─)</p>
</div>
