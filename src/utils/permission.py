
from twitchAPI.chat import ChatCommand
from functools import wraps

def permission(allowed_users: list):
    def decorator(func):
        func._is_public = (allowed_users is None)
        @wraps(func)
        async def wrapper(self, cmd: ChatCommand, *args, **kwargs):
            if func._is_public or (allowed_users is not None and cmd.user.name in allowed_users):
                return await func(self, cmd, *args, **kwargs)
            return
        return wrapper
    return decorator