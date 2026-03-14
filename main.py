import asyncio
from src.bot import Bot
from src.adapters.api.client import APIClient


async def update_data(shutdown_event: asyncio.Event, api_client: APIClient) -> None:
    while not shutdown_event.is_set():
        await asyncio.sleep(3600)
        await api_client.load_data()


async def main() -> None:
    shutdown_event = asyncio.Event()
    api_client = APIClient()
    bot = Bot(shutdown_event, api_client)
    await asyncio.gather(bot.run(), update_data(shutdown_event, api_client))


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
