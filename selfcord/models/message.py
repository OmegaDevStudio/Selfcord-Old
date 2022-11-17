from .user import User
import asyncio
import urllib

class Message:
    """Message Object
    """
    def __init__(self, data, bot, http) -> None:
        self.bot = bot
        self.channel = None
        self.guild = None
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.content}"

    def _update(self, data):
        self.tts = data.get("tts")
        self.referenced_message = data.get("referenced_message")
        self.mentions = data.get("mentions")
        self.author = User(data.get("author"), self.bot, self.http)
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.embeds = data.get("embeds")
        self.content = data.get("content")
        self.components = data.get("components")

        self.channel_id = data.get("channel_id")

        self.attachments = data.get("attachments")
        self.guild_id = data.get("guild_id")

        self.channel = self.bot.get_channel(self.channel_id)

        self.guild = self.bot.get_guild(self.guild_id)

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.channel_id}/messages/{self.id}")


    async def react(self, emoji):
        raw_reaction = urllib.parse.urlencode({"emoji": emoji}).split("emoji=")[1]
        await self.http.request(method="put", endpoint=f"/channels/{self.channel_id}/messages/{self.id}/reactions/{raw_reaction}/%40me?location=Message&burst=false", headers={"referer": f"https://discord.com/channels/@me/{self.channel_id}"})






