
from src.bot import Bot

if __name__ == "__main__":
    import asyncio
    
    bot = Bot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("bot stopped manually")