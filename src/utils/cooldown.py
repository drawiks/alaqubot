
from twitchAPI.chat import ChatCommand
import time

def cooldown(seconds=30, per_user=True):
    ignore_users = ["drawksr69", "alaqu1337"]
    def wrapper(func):
        async def inner(self, cmd: ChatCommand, *args, **kwargs):
            if cmd.user.name in ignore_users:
                return await func(self, cmd, *args, **kwargs)
            
            key = (cmd.user.name, func.__name__) if per_user else func.__name__
            now = time.time()
            
            if not hasattr(self, "_cooldowns"):
                self._cooldowns = {}
                last_used = self._cooldowns.get(key, 0)
                if now - last_used < seconds:
                    wait = round(seconds - (now - last_used), 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return
                
            self._cooldowns[key] = now
                
            return await func(self, cmd, *args, **kwargs)
        return inner
    return wrapper