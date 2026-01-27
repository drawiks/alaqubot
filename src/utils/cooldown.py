
from twitchAPI.chat import ChatCommand

from src.api import load_users

from functools import wraps
import time

def cooldown(seconds=30, per_user=True):
    ignore_users = load_users()["users"]
    cooldowns = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(self, cmd: ChatCommand, *args, **kwargs):
            if cmd.user.name in ignore_users:
                return await func(self, cmd, *args, **kwargs)

            key = (cmd.user.name, func.__name__) if per_user else func.__name__
            now = time.time()
            last = cooldowns.get(key, 0)
            if now - last < seconds:
                wait = round(seconds - (now - last), 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return
            cooldowns[key] = now
            return await func(self, cmd, *args, **kwargs)
        return wrapper
    return decorator
