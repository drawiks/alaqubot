
from typing import Any
import httpx, requests

from src.utils import logger

class APIClient:
    BASE_URL = "http://127.0.0.1:9090"
    
    def __init__(self):
        self.commands = self._data("commands")
        self.users = self._data("users")["users"]
        
        self.client = httpx.AsyncClient(timeout=10.0, http2=True)
    
    def _data(self, endpoint: str):
        try:
            response = requests.get(f"http://127.0.0.1:9090/data/{endpoint}", timeout=5)
            if response.status_code == 200:
                logger.success(f"success loading {endpoint} data")
                return response.json() 
        except Exception as e:
            logger.error(f"Сбой связи с API: {e}")
        return {}
        
    async def request(self, endpoint: str, arg: Any = None):
        query_services = ["currency", "cards", "translate"]
        url = f"{self.BASE_URL}/services/{endpoint}"
        params = {}
        
        if endpoint in query_services and arg:
            match endpoint:
                case "currency": key = "amount"
                case "cards": key = "count"
                case "translate": key = "text"
            params[key] = arg
        elif arg:
            url = f"{url}/{arg}"

        try:
            response = await self.client.get(url, params=params, timeout=10.0)
                
            if response.status_code == 200:
                logger.success(f"success fetching {endpoint}")
                data = response.json()
                return data.get("data")
            else:
                logger.error(f"API error {response.status_code} for {endpoint}")
                return "Ошибка на стороне API"
        except Exception as e:
            logger.error(f"Сбой связи с API: {e}")
            return "Сервер API временно недоступен"
        
client = APIClient()