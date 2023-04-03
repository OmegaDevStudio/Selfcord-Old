import asyncio
from typing import List, Union, Optional, Any, Dict

from .user import User
from .message import Message
from .webhook import Webhook
from ..api.http import Http


class Messageable:
    def __init__(self, http: Http, bot: Any) -> None:
        self.id = None
        self.http = http
        self.bot = bot

    async def history(self) -> Union[List[Message], List]:
        """
        Get channel message history.

        Args:
            No arguments required

        Returns:
            messages(list) : List of messages from the channel.
        """
        messages = []
        data = await self.http.request(method="get", endpoint=f"/channels/{self.id}/messages?limit=100")
        for msg in data:
            messages.append(Message(msg, self.bot, self.http))
        while True:
            data = await self.http.request(method="get",
                                           endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}")
            if len(data) > 0:
                for msg in data:
                    messages.append(Message(msg, self.bot, self.http))
            else:
                break

        return messages

    async def purge(self, amount: int = None):
        """
        Delete a number of messages, starting from the most recent.

        Args:
            amount(int) : Number of messages to purge/delete.

        Returns:
            No return value
        """
        messages = await self.history()
        msgs = []
        for msg in messages:
            if str(msg.author.id) == str(self.bot.user.id):
                msgs.append(msg)

        if amount is not None:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i + 3]))
        else:
            for i in range(0, len(msgs), 3):
                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i + 3]))

    #            for i in range(0, len(msgs[:amount]), 2):
    #                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[:amount][i:i + 2]))
    #                await asyncio.sleep(0.2)
    #        else:
    #            for i in range(0, len(msgs), 2):
    #                await asyncio.gather(*(asyncio.create_task(message.delete()) for message in msgs[i:i + 2]))
    #                await asyncio.sleep(0.2)

    async def spam(self, amount: int, content: str, tts=False):
        """
        Send multiple of the same message.

        Args:
            - amount(int) : Number of spam messages to send.
            - content(str) : The message to send.
            - tts(bool) = False : Specify whether it is a TTS message.

        Returns:
             No return value.
        """
        amount: list[int] = [i + 1 for i in range(amount)]
        for i in range(0, len(amount), 3):
            await asyncio.gather(
                *(asyncio.create_task(self.send(tts=tts, content=content)) for _ in amount[i:i + 3]))

    async def send(self, content=None, tts=False):
        """
        Send a message to the text channel.

        Args:
            - content(str) : Message content. Should be string type or similar. Discord `embed` type is not allowed.
            - tts(bool) :
        """
        if hasattr(self, "guild_id"):
            await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages",
                                    headers={"origin": "https://discord.com",
                                             "referer": f"https://discord.com/channels/{self.guild_id}/{self.id}"},
                                    json={"content": content, "tts": tts})
        else:
            await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages",
                                    headers={"origin": "https://discord.com",
                                             "referer": f"https://discord.com/channels/{self.id}"},
                                    json={"content": content, "tts": tts})

    async def reply(self, message, content=None, tts=False):
        if hasattr(self, "guild_id"):
            await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages",
                                    headers={"origin": "https://discord.com",
                                             "referer": f"https://discord.com/channels/{self.guild_id}/{self.id}"},
                                    json={"content": content, "tts": tts,
                                          "message_reference": {"channel_id": f"{self.id}",
                                                                "message_id": f"{message.id}"},
                                          "allowed_mentions": {"parse": ["users", "roles", "everyone"],
                                                               "replied_user": False}})
        else:
            await self.http.request(method="post", endpoint=f"/channels/{self.id}/messages",
                                    headers={"origin": "https://discord.com",
                                             "referer": f"https://discord.com/channels/{self.id}"},
                                    json={"content": content, "tts": tts,
                                          "message_reference": {"channel_id": f"{self.id}",
                                                                "message_id": f"{message.id}"},
                                          "allowed_mentions": {"parse": ["users", "roles", "everyone"],
                                                               "replied_user": False}})


class TextChannel(Messageable):
    """
    Text Channel Object
        Represents a Guild/Server channel within Discord.
        All methods are coroutines and thus need to be awaited.

    Returns:
        Name of the channel

    Functions:
        - delete()
        - edit(name[str], parent_id[int], position[int], topic[str])
        - history()
        - purge(amount[int])
        - spam(amount[int], content[str], tts[bool]=False)
        - send()
        - reply()
        - create_webhook()

    Example Object (ref: https://discord.com/developers/docs/resources/channel#channel-object-example-guild-text-channel)
        {
          "id": "41771983423143937",
          "guild_id": "41771983423143937",
          "name": "general",
          "type": 0,
          "position": 6,
          "permission_overwrites": [],
          "rate_limit_per_user": 2,
          "nsfw": true,
          "topic": "24/7 chat about how to gank Mike #2",
          "last_message_id": "155117677105512449",
          "parent_id": "399942396007890945",
          "default_auto_archive_duration": 60
        }
    """

    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        super().__init__(http, bot)
        self.permissions = []
        self.webhooks = []
        self.http = http
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data) -> None:
        self.topic = data.get("topic")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.last_message_id = data.get("last_message_id")
        self.flags = data.get("flags")
        self.default_thread_rate_limit_per_user = data.get("default_thread_rate_limit_per_user")
        self.category_id = data.get("parent_id")

    async def delete(self) -> None:
        """
        Deletes the text channel object.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

    async def edit(
        self, name: str = None, parent_id: int = None,
        position: int = None, topic: str = None
    ) -> Optional[str]:
        """
        Edits the text channel object details. Requires the `Manage Channels` permission.
        Not all details can be modified.

        Args:
            - name(str) : Optional - Specifies a new name for the channel object. Defaults to None.
            - parent_id(int) : Optional - Specifies a new parent (category) for the text channel object.
            - position(int) : Optional - Modifies the sorting position of the text channel within the guild.
            - topic(str) : Optional - Modifies the channel topic (0-4096 characters for GUILD_FORUM channels,
                                        0-1024 characters for all others)
        Notice: Each parent category can contain up to 50 channels.

        Returns:
            e(str) : Exception parsed as string value.
        """
        payload = {}
        if name is not None:
            payload['name'] = name
        if parent_id is not None:
            payload['parent_id'] = parent_id
        if position is not None:
            payload['position'] = position
        if topic is not None and topic != "":
            payload['topic'] = topic

        try:
            await self.http.request(method="patch", endpoint=f"/channels/{self.id}", json=payload)
        except Exception as e:
            from traceback import format_exception
            error = "".join(format_exception(type(e), e, e.__traceback__))
            return error

    async def create_webhook(self, name: str = None, avatar_url: str = None) -> Webhook:
        """
        Creates a webhook for the text channel object.

        Requires the `Manage Webhooks` permission.

        Args:
            name(str) : Specifies a new name for the webhook. Defaults to None.
            avatar_url(str) : (Optional) Specifies a new avatar for the webhook.

        Returns:
            The webhook object.
        """
        fields = {}
        if name is not None:
            fields['name'] = name
        else:
            raise TypeError("Name is required...")
        if avatar_url is not None:
            data = await self.http.encode_image(avatar_url)
            fields['avatar'] = data
        data = await self.http.request(method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields)
        self.webhooks.append(Webhook(data, self.bot, http=self.http))
        return Webhook(data, self.bot, http=self.http)


class VoiceChannel(Messageable):
    """Voice Channel Object"""

    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        super().__init__(http, bot)
        self.permissions = []
        self.webhooks = []
        self.http = http
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data) -> None:
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

    async def delete(self) -> None:
        """
        Deletes the voice channel.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

    async def create_webhook(self, name: str = None, avatar_url: str = None) -> Webhook:
        """
        Creates a webhook for the voice channel.

        Requires the `Manage Webhooks` permission.

        Args:
            name(str): Specifies a new name for the webhook. Defaults to None.

            avatar_url(str) : (Optional) Specifies a new avatar for the webhook.

        Returns:
            The webhook object
        """
        fields = {}
        if name is not None:
            fields['name'] = name
        else:
            raise TypeError("Name is required...")
        if avatar_url is not None:
            data = await self.http.encode_image(avatar_url)
            fields['avatar'] = data
        data = await self.http.request(method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields)
        webhook = Webhook(data, self.bot, self.http)
        self.webhooks.append(webhook)
        return webhook

    async def call(self) -> None:
        """
        Calls the voice channel.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.ring(self.id, self.guild_id)

    async def leave(self) -> None:
        """
        Leaves the voice channel.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.leave_call()


class Category:
    """Category Object
    """

    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        self.bot = bot
        self.http = http
        self.permissions = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data) -> None:
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.position = data.get("position")
        self.flags = data.get("flags")

    async def delete(self) -> None:
        """
        Deletes the category.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self


class DMChannel(Messageable):
    """DM Channel Object
    """

    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        super().__init__(http, bot)
        self.http = http
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.recipient}"

    def _update(self, data) -> None:
        self.recipient = User(data.get("recipients")[0], self.bot, self.http)
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("id")

    async def delete(self, silent: bool = False) -> None:
        """
        Leaves from the DM channel.

        Args:
            silent(bool): (Optional) If true, you leave from channel without information about leaving. Defaults False.

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}?silent={'true' if silent else 'false'}")
        del self

    async def leave_channel(self) -> None:
        """
        Alias of the `delete` method.
        """
        await self.delete()

    async def call(self) -> None:
        """
        Calls the DM channel.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.ring(self.id)

    async def leave(self) -> None:
        """
        Leaves from the call.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.leave_call()


class GroupChannel(Messageable):
    """Group Channel Object"""

    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        super().__init__(http, bot)
        self.recipients = []
        self.http = http
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data) -> None:
        for user in data.get("recipients"):
            self.recipients.append(User(user, self.bot, self.http))
        self.name = data.get("name")
        self.owner_id = data.get("owner_id")
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.icon = data.get("icon")

    async def delete(self, silent: bool = False) -> None:
        """
        Leaves from the group channel.

        Args:
            silent(bool): (Optional) If true, you leave from channel without information about leaving. Defaults False.

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}?silent={'true' if silent else 'false'}")
        del self

    async def call(self) -> None:
        """
        Calls on the group channel.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.ring(self.id)

    async def leave(self):
        """
        Leaves from the call.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.bot.Gateway.leave_call()
