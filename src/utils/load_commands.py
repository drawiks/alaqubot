
import json, os

def load_commands():
    path = "commands.json"
    if not os.path.exists(path):
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)