
commands = {}

def register(name: str):
    def decorator(func):
        commands[name] = func
        return func
    return decorator