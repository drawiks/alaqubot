import os
from pathlib import Path
from typing import Any, Optional

import yaml
from environs import Env


def _find_base_path() -> Path:
    if os.environ.get("DOCKER_MODE"):
        return Path("/app")
    return Path(__file__).parent.parent


def load_env() -> None:
    env = Env()
    env_path = os.environ.get("ENV_PATH")

    if env_path:
        path = Path(env_path)
    else:
        path = _find_base_path() / ".env"

    if path.exists():
        env.read_env(str(path))


load_env()

env = Env()

CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
TOKEN = env.str("TOKEN")
REFRESH_TOKEN = env.str("REFRESH_TOKEN")
BOT_ID = env.str("BOT_ID")
CHANNELS = env.list("CHANNELS", subcast=str.lower)
LOG_PATH = env.str("LOG_PATH")

RATE_LIMIT_GLOBAL = env.int("RATE_LIMIT_GLOBAL", 30)
RATE_LIMIT_USER = env.int("RATE_LIMIT_USER", 15)

LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
LOG_ROTATION = env.str("LOG_ROTATION", "10MB")
LOG_RETENTION = env.str("LOG_RETENTION", "7 days")


def get_plugin_config(plugin_name: str) -> dict[str, Any]:
    base_path = _find_base_path()
    config_path = base_path / "src" / "plugins" / plugin_name / "config.yaml"

    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def get_config_path() -> Path:
    return _find_base_path() / "config"
