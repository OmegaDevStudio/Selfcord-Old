from .message import Message
import time
from .user import User
from .webhook import Webhook
import asyncio

from selfcord.models import message

class TextChannel:
    """Text Channel Object
    """
    def __init__(self, data, bot, http) -> None:
        self.permissions = []
        self.webhooks = []
        self.http = http
        self.bot = bot
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

    async def history(self):
        messages = []
        data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100")
        for msg in data:
            messages.append(Message(msg, self.bot, self.http))
        while True:
            data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}")
            if len(data) > 0:
                for msg in data:
                    messages.append(Message(msg, self.bot, self.http))
            else:
                break

        return messages

    async def purge(self, amount: int=None):
        messages = await self.history()
        msgs = []
        for msg in messages:
            if str(msg.author.id) == str(self.bot.user.id):
                msgs.append(msg)

        if amount != None:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i+3]))
        else:
            for i in range(0, len(msgs), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i+3]))

    async def spam(self, amount: int,  content: str, tts= False):
        amount: list[int] = [i+1 for i in range(amount)]
        for i in range(0, len(amount), 3):
            await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for amoun in amount[i:i+3]))

    async def send(self,  content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})

    async def create_webhook(self, name: str=None, avatar_url: str=None):
        fields = {}
        if name != None:
            fields['name'] = name
        else:
            raise TypeError("Name is required...")
        if avatar_url != None:
            data = await self.http.encode_image(avatar_url)
            fields['avatar'] = data
        data = await self.http.request(method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields)
        self.webhooks.append(Webhook(data, self.http))



class VoiceChannel:
    """Voice Channel Object
    """
    def __init__(self, data, bot, http) -> None:
        self.permissions = []
        self.webhooks = []
        self.http = http
        self.bot = bot
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

    async def history(self):
        messages = []
        data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100")
        for msg in data:
            messages.append(Message(msg, self.bot, self.http))
        while True:
            data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}")
            if len(data) > 0:
                for msg in data:
                    messages.append(Message(msg, self.bot, self.http))
            else:
                break

        return messages

    async def purge(self, amount: int=None):
        messages = await self.history()
        msgs = []
        for msg in messages:
            if str(msg.author.id) == str(self.bot.user.id):
                msgs.append(msg)

        if amount != None:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i+3]))
        else:
            for i in range(0, len(msgs), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i+3]))

    async def spam(self, amount: int,  content: str, tts= False):
        amount: list[int] = [i+1 for i in range(amount)]
        for i in range(0, len(amount), 3):
            await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for amoun in amount[i:i+3]))

    async def send(self,  content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})

    async def create_webhook(self, name: str=None, avatar_url: str=None):
        fields = {}
        if name != None:
            fields['name'] = name
        else:
            raise TypeError("Name is required...")
        if avatar_url != None:
            data = await self.http.encode_image(avatar_url)
            fields['avatar'] = data
        data = await self.http.request(method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields)
        self.webhooks.append(Webhook(data, self.http))



class Category:
    """Category Object
    """
    def __init__(self, data, bot, http) -> None:
        self.bot = bot
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
    def __init__(self, data, bot, http) -> None:
        self.http = http
        self.bot = bot
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

    async def history(self):
        messages = []
        data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100")
        for msg in data:
            messages.append(Message(msg, self.bot, self.http))
        while True:
            data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}")
            if len(data) > 0:
                for msg in data:
                    messages.append(Message(msg, self.bot, self.http))
            else:
                break

        return messages

    async def purge(self, amount: int=None):
        messages = await self.history()
        msgs = []
        for msg in messages:
            if str(msg.author.id) == str(self.bot.user.id):
                msgs.append(msg)

        if amount != None:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i+3]))
        else:
            for i in range(0, len(msgs), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i+3]))

    async def spam(self, amount: int,  content: str, tts= False):
        amount: list[int] = [i+1 for i in range(amount)]
        for i in range(0, len(amount), 3):
            await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for amoun in amount[i:i+3]))

    async def send(self, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})

class GroupChannel:
    """Group Channel Object
    """
    def __init__(self, data, bot, http) -> None:
        self.recipients = []
        self.http = http
        self.bot = bot
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

    async def history(self):
        messages = []
        data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100")
        for msg in data:
            messages.append(Message(msg, self.bot, self.http))
        while True:
            data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}")
            if len(data) > 0:
                for msg in data:
                    messages.append(Message(msg, self.bot, self.http))
            else:
                break

        return messages

    async def purge(self, amount: int=None):
        messages = await self.history()
        msgs = []
        for msg in messages:
            if str(msg.author.id) == str(self.bot.user.id):
                msgs.append(msg)

        if amount != None:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i+3]))
        else:
            for i in range(0, len(msgs), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i+3]))

    async def spam(self, amount: int,  content: str, tts= False):
        amount: list[int] = [i+1 for i in range(amount)]
        for i in range(0, len(amount), 3):
            await asyncio.gather(*(asyncio.create_task(self.send(tts=tts, content=content)) for amoun in amount[i:i+3]))
            
    async def send(self, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages", json={"content": content, "tts": tts, "message_reference": {"channel_id": f"{self.id}", "message_id": f"{message.id}"}, "allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": False}})





