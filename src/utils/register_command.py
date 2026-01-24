
from typing import Dict, Tuple, Callable

_commands: Dict[str, Tuple[Callable, str, bool]] = {}

def register(name: str):
    def decorator(func: Callable):
        qual = getattr(func, "__qualname__", "")
        owner = qual.split(".")[0] if "." in qual else ""
        is_public = getattr(func, "_is_public", True)
        _commands[name] = (func, owner, is_public)
        return func
    return decorator

def get_commands():
    return dict(_commands)
