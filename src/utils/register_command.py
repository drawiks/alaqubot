
from typing import Callable, Optional
import inspect

def register(name: str, allowed_users: Optional[list]):
    def decorator(func: Callable):
        func._is_public = allowed_users is None
        func._is_command = True
        func._name = name
        return func
    return decorator

def get_methods(instance):
    commands = []
    for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
        if hasattr(method, "_is_command"):
            commands.append({
                "name": method._name,
                "func": method,
                "public": method._is_public
            })
    return commands
