import time
from .user import User
from selfcord.api.http import http
import asyncio

class TextChannel:
    """Text Channel Object
    """
    def __init__(self, data, http) -> None:
        self.permissions = []
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.topic = data.get("topic")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.last_message_id= data.get("last_message_id")
        self.flags = data.get("flags")
        self.default_thread_rate_limit_per_user = data.get("default_thread_rate_limit_per_user")
        self.category_id = data.get("parent_id")

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

    async def spam(self, amount: int,  content: str, tts= False):
        await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for i in range(int(amount))))

    async def send(self,  content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})


class VoiceChannel:
    """Voice Channel Object
    """
    def __init__(self, data, http) -> None:
        self.permissions = []
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.last_message_id = data.get("last_message_id")
        self.rtc_region = data.get("rtc_region")
        self.flags = data.get("flags")
        self.bitrate = data.get("bitrate")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.category_id = data.get("parent_id")

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

    async def spam(self, amount: int,  content: str, tts= False):
        await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for i in range(int(amount))))

    async def send(self,  content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})

class Category:
    """Category Object
    """
    def __init__(self, data, http) -> None:
        self.http = http
        self.permissions = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.position = data.get("position")
        self.flags = data.get("flags")

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

class DMChannel:
    """DM Channel Object
    """
    def __init__(self, data, http) -> None:
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.recipient}"

    def _update(self, data):
        self.recipient = User(data.get("recipients")[0])
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("id")

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}?silent=false")
        del self

    async def spam(self, amount: int,  content: str, tts= False):
        await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for i in range(int(amount))))

    async def send(self, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})

class GroupChannel:
    """Group Channel Object
    """
    def __init__(self, data, http) -> None:
        self.recipients = []
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        for user in data.get("recipients"):
            self.recipients.append(User(user))
        self.name = data.get("name")
        self.owner_id = data.get("owner_id")
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.icon = data.get("icon")

    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}?silent=true")
        del self

    async def spam(self, amount: int,  content: str, tts= False):
        for i in range(0, amount, 6):
            await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for i in range(int(i))))

    async def send(self, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})


