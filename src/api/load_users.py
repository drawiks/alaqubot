
import requests

def load_users():
    try:
        response = requests.get("http://127.0.0.1:9090/users")
        if response:
            return response.json() 
    except Exception as e:
        pass
    return {}