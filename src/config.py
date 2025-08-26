from environs import Env
from pathlib import Path
import sys

env = Env()

if getattr(sys, "frozen", False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

env.read_env(str(base_path / ".env"))

CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
TOKEN = env.str("TOKEN")
REFRESH_TOKEN = env.str("REFRESH_TOKEN")
OWNER_ID = env.str("OWNER_ID")
BOT_ID = env.str("BOT_ID")
CHANNEL = env.str("CHANNEL")
LOG_PATH = env.str("LOG_PATH")
