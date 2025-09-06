from twitchAPI.chat import ChatCommand
import time

def cooldown(seconds=30, per_user=True):
    ignore_users = ["drawksr69", "alaqu1337"]
    cooldowns = {}
    def wrapper(func):
        async def inner(cmd: ChatCommand, *args, **kwargs):
            if cmd.user.name in ignore_users:
                return await func(cmd, *args, **kwargs)

            key = (cmd.user.name, func.__name__) if per_user else func.__name__
            now = time.time()
            last_used = cooldowns.get(key, 0)
            elapsed = now - last_used

            if elapsed < seconds:
                wait = round(seconds - elapsed, 1)
                await cmd.reply(f"Подожди {wait} сек!")
                return

            cooldowns[key] = now

            return await func(cmd, *args, **kwargs)
        return inner
    return wrapper
