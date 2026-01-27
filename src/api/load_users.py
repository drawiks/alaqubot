
import requests

def load_users():
    try:
        response = requests.get("http://127.0.0.1:9090/users")
        if response.status_code == 200:
            return response.json() 
    except Exception as e:
        pass
    return {}