
from .commands import Commands

import importlib
import pkgutil
import inspect

def load_groups(package_path: str, package_name: str):
    groups = []
    
    for _, name, is_pkg in pkgutil.iter_modules([package_path]):
        if is_pkg: continue
        module = importlib.import_module(f"{package_name}.{name}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, Commands) and cls is not Commands:
                groups.append(cls())      
    return groups