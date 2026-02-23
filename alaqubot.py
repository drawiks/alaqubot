from src.bot import Bot
from src.api import client
import asyncio
import signal

async def update_data():
    while True:
        await asyncio.sleep(3600)
        await client.load_data()

async def main():
    bot = Bot()
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, bot.stop)
    
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