# 🔌 Plugin API

Полный справочник по методам и свойствам базового класса `Plugin`.

## Базовый класс

```python
from src.core.plugin import Plugin


class MyPlugin(Plugin):
    ...
```

## Обязательные атрибуты

Каждый плагин должен определять:

```python
class MyPlugin(Plugin):
    name: str = "myplugin"      # Уникальное имя
    version: str = "1.0.0"     # Версия плагина
```

## Обязательные методы

### on_load()

Вызывается при загрузке плагина.

```python
async def on_load(self) -> None:
    # Инициализация
    print(f"Плагин {self.name} загружен!")
```

### on_unload()

Вызывается при выгрузке плагина.

```python
async def on_unload(self) -> None:
    # Очистка ресурсов
    print(f"Плагин {self.name} выгружен!")
```

### get_commands()

Возвращает список команд плагина.

```python
def get_commands(self) -> list[dict]:
    return [
        {
            "name": "команда",           # Имя команды
            "handler": self.my_handler, # Функция-обработчик
            "config": {...}             # Конфиг команды
        },
    ]
```

## Свойства (Properties)

### self.enabled

Возвращает `True` если плагин включен.

```python
if self.enabled:
    print("Плагин включен!")
```

### self.client

Доступ к API клиенту.

```python
# Получить данные от API
result = await self.client.request("currency")

# Отправить запрос
response = await self.client.post_request("endpoint", {"key": "value"})
```

### self.users

Список пользователей с правами.

```python
if username in self.users:
    # Пользователь имеет права
    pass
```

### self.commands_config

Конфигурация всех команд плагина.

```python
config = self.commands_config
```

### self.settings

Кастомные настройки из YAML.

```python
value = self.settings.get("my_option", "default")
```

## Методы

### check_permission(username: str) -> bool

Проверяет права пользователя.

```python
if self.check_permission(cmd.user.name):
    # Выполнить действие для модеров
    await cmd.reply("У вас есть права!")
else:
    await cmd.reply("У вас нет прав!")
```

### get_command_config(cmd_name: str) -> dict

Получает конфиг конкретной команды.

```python
config = self.get_command_config("моя_команда")
cooldown = config.get("cooldown", 0)
enabled = config.get("enabled", True)
```

## Объект команды (cmd)

Каждый обработчик получает объект `cmd`:

### cmd.user

Информация о пользователе.

```python
cmd.user.name       # Имя пользователя
cmd.user.id         # ID пользователя
```

### cmd.room

Информация о канале.

```python
cmd.room.name       # Имя канала
```

### cmd.parameter

Параметры команды.

```python
# !погода Киев
cmd.parameter  # "Киев"
```

### cmd.reply(text: str)

Отправить ответ в чат.

```python
await cmd.reply("Привет!")
```

### cmd.send(text: str)

Отправить сообщение (без упоминания).

```python
await cmd.send("Сообщение")
```

## Пример использования API

```python
from src.core.plugin import Plugin


class MyPlugin(Plugin):
    name = "myplugin"
    version = "1.0.0"

    async def on_load(self) -> None:
        # Проверка что плагин включен
        if not self.enabled:
            return
        print("Плагин загружен!")

    def get_commands(self) -> list[dict]:
        return [
            {"name": "тест", "handler": self.test, "config": self.get_command_config("тест")},
            {"name": "апи", "handler": self.api_test, "config": self.get_command_config("апи")},
        ]

    async def test(self, cmd):
        await cmd.reply(f"Привет, {cmd.user.name}!")

    async def api_test(self, cmd):
        # Используем API
        result = await self.client.request("currency")
        await cmd.reply(f"Курс доллара: {result}")
```

---

## Следующие шаги

- [Примеры](Примеры) - Готовые примеры плагинов
- [Распространение](Распространение) - Как делиться плагинами
