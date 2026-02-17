
from src.bot import Bot

if __name__ == "__main__":
    import asyncio
    
    from pyfiglet import figlet_format
    from dcolor import color
    
    print(color(figlet_format("AlaquBot", font="larry3d"), "#4caf50"))
    
    try:
        bot = Bot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("bot stopped manually")
    except Exception as e:
        print(f"bot stopped with error: {e}")