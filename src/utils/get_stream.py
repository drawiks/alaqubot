
async def get_stream(self, channel):
    async for user in self.twitch.get_users(logins=[channel]):
        user_id = user.id
        found = False
        async for stream in self.twitch.get_streams(user_id=[user_id]):
            data = {
                "status":"online",
                "title":stream.title,
                "viewer_count":stream.viewer_count,
                "game_name":stream.game_name
            }
            found = True
            return data
        if not found:
            return "❌ Стрим оффлайн"