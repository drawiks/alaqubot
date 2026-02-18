
from cachetools import TTLCache
from functools import wraps
import time

def cooldown(seconds=30, per_user=True):
    cooldowns = TTLCache(maxsize=1000, ttl=seconds)
    def decorator(func):
        @wraps(func)
        async def wrapper(self, cmd, *args, **kwargs):
            ignore_users = self.client.users
            if cmd.user.name in ignore_users:
                return await func(self, cmd, *args, **kwargs)

            key = (cmd.user.name, func.__name__) if per_user else func.__name__
            if key in cooldowns:
                wait = round(seconds - (time.time() - cooldowns[key]), 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return
            
            cooldowns[key] = time.time()
            
            return await func(self, cmd, *args, **kwargs)
        return wrapper
    return decorator