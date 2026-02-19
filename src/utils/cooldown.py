from functools import wraps
import time

from .cache import CacheManager

def cooldown(seconds=30, per_user=True):
    cooldowns = CacheManager(maxsize=1000, ttl=seconds)

    def decorator(func):
        @wraps(func)
        async def wrapper(self, cmd, *args, **kwargs):
            ignore_users = self.client.users
            if cmd.user.name in ignore_users:
                return await func(self, cmd, *args, **kwargs)

            key = f"{cmd.user.name}:{func.__name__}" if per_user else func.__name__
            last = cooldowns.get_cache(key)

            if last is not None:
                wait = round(seconds - (time.time() - last), 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return

            cooldowns.set_cache(key, time.time())
            return await func(self, cmd, *args, **kwargs)
        return wrapper
    return decorator