
import httpx
from pathlib import Path

from .logger import logger

class AuthManager:
    _instance = None
    
    def __new__(cls, env_path: Path = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, env_path: Path = None):
        if self._initialized:
            return
        self._env_path = env_path
        self._token = None
        self._refresh_token = None
        self._initialized = True
    
    def load_tokens(self, token: str, refresh_token: str):
        self._token = token
        self._refresh_token = refresh_token
    
    async def refresh(self, client_id: str, client_secret: str) -> bool:
        try:
            async with httpx.AsyncClient() as http:
                response = await http.post(
                    "https://id.twitch.tv/oauth2/token",
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": self._refresh_token,
                        "client_id": client_id,
                        "client_secret": client_secret,
                    },
                )
                if response.status_code == 200:
                    data = response.json()
                    self._token = data["access_token"]
                    self._refresh_token = data.get("refresh_token", self._refresh_token)
                    self._save_tokens_to_env()
                    logger.success("token refreshed")
                    return True
                else:
                    logger.error(f"token refresh failed: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"token refresh error: {e}")
            return False
    
    def _save_tokens_to_env(self):
        try:
            if self._env_path.exists():
                lines = self._env_path.read_text().splitlines()
                new_lines = []
                for line in lines:
                    if line.startswith("TOKEN="):
                        new_lines.append(f"TOKEN={self._token}")
                    elif line.startswith("REFRESH_TOKEN="):
                        new_lines.append(f"REFRESH_TOKEN={self._refresh_token}")
                    else:
                        new_lines.append(line)
                self._env_path.write_text("\n".join(new_lines) + "\n")
                logger.info("tokens saved to .env")
        except Exception as e:
            logger.error(f"failed to save tokens: {e}")
