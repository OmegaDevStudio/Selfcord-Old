from selfcord.models import channel
from .user import User
import asyncio

class Message:
    def __init__(self, data, bot) -> None:
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.content}"

    def _update(self, data):
        self.tts = data.get("tts")
        self.references_message = data.get("referenced_message")
        self.mentions = data.get("mentions")
        self.author = User(data.get("author"))
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.embeds = data.get("embeds")
        self.content = data.get("content")
        self.components = data.get("components")

        channel_id = data.get("channel_id")

        self.attachments = data.get("attachments")
        guild_id = data.get("guild_id")
        async def runner():
            self.channel = await self.bot.get_channel(channel_id)
            self.guild = await self.bot.get_guild(guild_id)
        asyncio.create_task(runner())



