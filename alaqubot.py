from src.app import main


if __name__ == "__main__":
    import asyncio
    from src.depends import twitch_session, chat

    asyncio.run(
        main(
            session=twitch_session,
            chat=chat,
        )
    )