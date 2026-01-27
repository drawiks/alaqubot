
import requests

def load_commands():
    try:
        response = requests.get("http://127.0.0.1:9090/commands")
        if response:
            return response.json() 
    except Exception as e:
        pass
    return {}