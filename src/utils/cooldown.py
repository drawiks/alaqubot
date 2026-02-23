
from functools import wraps
import time

from .cache import cache
from .logger import logger

_cooldown_storage = {}

def cooldown(seconds=30, per_user=True):

    def decorator(func):
        @wraps(func)
        async def wrapper(self, cmd, *args, **kwargs):
            logger.trace(f"cmd: {func.__name__} | {cmd.user.name}")
            
            ignore_users = self.client.users
            if cmd.user.name in ignore_users:
                return await func(self, cmd, *args, **kwargs)
            
            key = f"{cmd.user.name}:{func.__name__}" if per_user else func.__name__
            now = time.time()
            last = _cooldown_storage.get(key)
            
            if last is not None and now - last < seconds:
                wait = round(seconds - (now - last), 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return
            
            _cooldown_storage[key] = now
            
            expired = [k for k, v in _cooldown_storage.items() if now - v >= seconds]
            for k in expired:
                del _cooldown_storage[k]
            
            return await func(self, cmd, *args, **kwargs)
        return wrapper
    return decorator