from environs import env

env.read_env()

CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")

TOKEN = env.str("TOKEN")
REFRESH_TOKEN = env.str("REFRESH_TOKEN")

OWNER_ID = env.str("OWNER_ID")
BOT_ID = env.str("BOT_ID")

CHANNEL = env.str("CHANNEL")

LOG_PATH = env.str("LOG_PATH")