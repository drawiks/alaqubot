from typing import Any
import asyncio
import httpx

from src.utils.logger import logger


class APIClient:
    BASE_URL = "http://127.0.0.1:9090"

    def __init__(self) -> None:
        self.commands: dict[str, Any] = {}
        self.users: list[str] = []
        self.client = httpx.AsyncClient(timeout=10.0, http2=True)

    async def close(self) -> None:
        await self.client.aclose()

    async def load_data(self, retries: int = 3, delay: int = 5) -> None:
        for attempt in range(retries):
            try:
                commands = await self._async_data("commands")
                users_data = await self._async_data("users")
                self.commands = commands or {}
                self.users = users_data.get("users", []) if users_data else []
                logger.success("data loaded")
                return
            except Exception as e:
                logger.warning(f"attempt {attempt+1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
        logger.error("Failed to load data after retries")

    async def _async_data(self, endpoint: str) -> dict | None:
        response = await self.client.get(f"{self.BASE_URL}/data/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}

    async def request(self, endpoint: str, arg: Any = None) -> Any:
        query_services = {
            "currency": "amount",
            "cards": "count",
            "translate": "text",
            "wiki": "article",
        }
        url = f"{self.BASE_URL}/services/{endpoint}"
        params: dict[str, Any] = {}
        key = ""

        if endpoint in query_services and arg:
            key = query_services[endpoint]
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
            logger.error(f"API connection failed: {e}")
            return "Сервер API временно недоступен"

    async def post_request(self, endpoint: str, data: dict) -> Any:
        url = f"{self.BASE_URL}/services/{endpoint}"

        try:
            response = await self.client.post(url, json=data, timeout=15.0)

            if response.status_code == 200:
                logger.success(f"success fetching {endpoint}")
                res_data = response.json()
                return res_data.get("data")
            else:
                logger.error(f"API error {response.status_code} for {endpoint}")
                return "Ошибка ИИ на стороне сервера"
        except Exception as e:
            logger.error(f"API connection failed (POST): {e}")
            return "Мозг бота сейчас не в сети"
