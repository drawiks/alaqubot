
from src.bot import Bot

if __name__ == "__main__":
    import asyncio
    
    bot = Bot()
    asyncio.run(bot.run())