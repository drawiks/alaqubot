
from src.bot import Bot
from src.api import client
import asyncio

async def update_data():
    while not Bot._shutdown:
        await asyncio.sleep(3600)
        await client.load_data()

async def main():
    bot = Bot()
    await asyncio.gather(bot.run(), update_data())

if __name__ == "__main__":
    from pyfiglet import figlet_format
    from dcolor import color
    
    print(color(figlet_format("AlaquBot", font="larry3d"), "#4caf50"))
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot stopped manually")
    except Exception as e:
        print(f"bot stopped with error: {e}")