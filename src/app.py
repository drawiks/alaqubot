
from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat


async def main(
    session: Twitch,
    chat: Chat
) -> None:
    await session
    await chat

    chat.start()


if __name__ == "__main__":
    import asyncio
    from depends import twitch_session, chat

    asyncio.run(
        main(
            session=twitch_session,
            chat=chat,
        )
    )