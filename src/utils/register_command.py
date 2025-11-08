
from typing import Dict, Tuple, Callable

_commands: Dict[str, Tuple[Callable, str]] = {}

def register(name: str):
    def decorator(func: Callable):
        qual = getattr(func, "__qualname__", "")
        owner = qual.split(".")[0] if "." in qual else ""
        _commands[name] = (func, owner)
        return func
    return decorator

def get_commands():
    return dict(_commands)
