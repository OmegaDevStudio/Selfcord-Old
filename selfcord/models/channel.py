from __future__ import annotations

import asyncio
import os
import random
from traceback import format_exception
from typing import TYPE_CHECKING

import aiofiles
import aiohttp

from ..utils import logging
from .message import Message
from .user import User
from .webhook import Webhook

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot
    from ..models.permission import Permission

log = logging.getLogger("Channel")


class Messageable:
    """Parent class specific for those classes that include a textchat for sending messages."""

    def __init__(self, http: http, bot: Bot) -> None:
        self.http: http = http
        self.bot: Bot = bot

    @property
    def make_nonce(self):
        """Generate pseudorandom number."""
        return str(random.randint(0, 100000000))

    async def history(self, amount: int = 100) -> list[Message] | None:
        """
        Get channel message history.

        Args:
            amount(int) : Amount of messages to gather. Default is 100.

        Returns:
            messages(list) : List of messages from the channel.
            None : If client does not have view permission for the channel or no data found
        """
        if amount >= 100:
            data = await self.http.request(
                method="get", endpoint=f"/channels/{self.id}/messages?limit=100"
            )
        else:
            data = await self.http.request(
                method="get", endpoint=f"/channels/{self.id}/messages?limit={amount + 5}"
            )

        if data is None:
            return None

        messages = [Message(msg, self.bot, self.http) for msg in data]
        while True:
            

            data = await self.http.request(
                method="get",
                endpoint=f"/channels/{self.id}/messages?limit=100&before={data[-1]['id']}",
            )

            if len(data) <= 0:
                break
            messages.extend(Message(msg, self.bot, self.http) for msg in data)
            if len(messages) >= amount:
                break

        return messages

    async def upload_image(self, paths: list[str]) -> list[dict[str, int | str]]:
        files = []
        id = 0
        for path in paths:
            async with aiofiles.open(path, "rb") as f:
                file = await f.read()
                size = len(file)
                name = os.path.basename(path)
            files.append({"file_size" : size, "filename": f"{name}", "id": id})
            id += 1
        json = await self.http.request("post", f"/channels/{self.id}/attachments", json={"files": files})
        items = []
        for key, atch in enumerate(json['attachments']):
            upload_url = atch['upload_url']
            id = atch['id']
            upload_filename = atch['upload_filename']
            async with aiohttp.ClientSession() as session:
                async with aiofiles.open(paths[key], "rb") as f:
                    file = await f.read()
                async with session.put(upload_url, data=file): 
                    pass
            items.append({"uploaded_filename": upload_filename, "filename": os.path.basename(upload_filename) , "id": id})
        return items

        

    async def purge(self, amount: int = 0) -> None:
        """
        Delete a number of messages, starting from the most recent.

        Args:
            amount(int) : Number of messages to purge/delete.

        Returns:
            No return value
        """
        messages = await self.history(amount)
        if messages is None:
            return
        msgs = [msg for msg in messages if str(msg.author.id) == str(self.bot.user.id)]
        if amount != 0:
            for i in range(0, len(msgs[:amount]), 3):
                await asyncio.gather(
                    *(
                        asyncio.create_task(message.delete())
                        for message in msgs[:amount][i : i + 3]
                    )
                )
                await asyncio.sleep(0.3)
            return


        for i in range(0, len(msgs), 3):
            await asyncio.gather(
                *(
                    asyncio.create_task(message.delete())
                    for message in msgs[i : i + 3]
                )
            )
            await asyncio.sleep(0.3)



    async def spam(self, amount: int, content: str, file_paths: list[str] = [], tts=False) -> None:
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
                *(
                    asyncio.create_task(self.send(tts=tts, content=content, file_paths=file_paths))
                    for _ in amount[i : i + 3]
                )
            )
            await asyncio.sleep(0.3)

    async def send(self, content=None, file_paths: list[str] = [], tts=False) -> Message:
        """
        Send a message to the text channel.

        Args:
            - content(str) : Message content. Should be string type or similar. Discord `embed` type is not allowed.
            - tts(bool) : Specify whether message is text-to-speech or not

        Returns:
            Message object.
        """
        json = {"content": content, "nonce": self.make_nonce, "tts": tts}
        if file_paths != []:
            vals = await self.upload_image(file_paths)
            json |= {"attachments" : vals}

        if hasattr(self, "guild_id"):
            resp = await self.http.request(
                method="post",
                endpoint=f"/channels/{self.id}/messages",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.guild_id}/{self.id}",
                },
                json=json
            )
            resp.update({"guild_id": self.guild_id})

        else:
            resp = await self.http.request(
                method="post",
                endpoint=f"/channels/{self.id}/messages",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.id}",
                },
                json=json
            )

        return Message(resp, self.bot, self.http)

    async def reply(self, message: Message, content: str, file_paths: list[str] = [], tts=False) -> Message:
        """Reply to a specific message

        Args:
            message (str): Message to reply to
            content (_type_, optional): Message content to reply with. Defaults to None.
            tts (bool, optional): Specify whether message is text-to-speech or not. Defaults to False.

        Returns:
            Message object.
        """
        json = {
            "content": content,
            "tts": tts,
            "nonce": self.make_nonce,
            "message_reference": {
                "channel_id": f"{self.id}",
                "message_id": f"{message.id}",
            },
        }

        if file_paths != []:
            vals = await self.upload_image(file_paths)
            json |= {"attachments" : vals}

        if hasattr(self, "guild_id"):
            resp = await self.http.request(
                method="post",
                endpoint=f"/channels/{self.id}/messages",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.guild_id}/{self.id}",
                },
                json=json
            )
            resp.update({"guild_id": self.guild_id})
        else:
            resp = await self.http.request(
                method="post",
                endpoint=f"/channels/{self.id}/messages",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.id}",
                },
                json=json
            )
        return Message(resp, self.bot, self.http)


class Voiceable(Messageable):
    """Parent class specific for those classes that include a voice chat, or call functionality"""

    def __init__(self, http: http, bot: Bot) -> None:
        super().__init__(http, bot)
        self.http: http = http
        self.bot: Bot = bot

    async def video_call(self):
        """Initiates a video call on the specified channel"""
        if hasattr(self, "guild_id"):
            await self.bot.gateway.video_call(self.id, self.guild_id)
        else:
            await self.bot.gateway.video_call(self.id)

    async def stream_call(self):
        """Initiates a stream call on the specified channel"""
        if hasattr(self, "guild_id"):
            await self.bot.gateway.stream_call(self.id, self.guild_id)
        else:
            await self.bot.gateway.stream_call(self.id)

    async def call(self):
        """Initiates a call on the specified channel"""

        if hasattr(self, "guild_id"):
            await self.bot.gateway.call(self.id, self.guild_id)
        else:
            await self.bot.gateway.call(self.id)

    async def leave_call(self):
        """Leaves call on the specified channel"""
        await self.bot.gateway.leave_call()


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

    def __init__(self, data, bot: Bot, http: http) -> None:
        super().__init__(http, bot)
        self.permissions: list[Permission] = []
        self.webhooks: list[Webhook] = []
        self.http: http = http
        self.bot: Bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """

        self.topic = data.get("topic")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.last_message_id = data.get("last_message_id")
        self.flags = data.get("flags")
        self.default_thread_rate_limit_per_user = data.get(
            "default_thread_rate_limit_per_user"
        )
        self.category_id = data.get("parent_id")

    async def delete(self):
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
        self,
        name: str = None,
        parent_id: int = None,
        position: int = None,
        topic: str = None,
    ):
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
            payload["name"] = name
        if parent_id is not None:
            payload["parent_id"] = parent_id
        if position is not None:
            payload["position"] = position
        if topic is not None and topic != "":
            payload["topic"] = topic

        try:
            await self.http.request(
                method="patch", endpoint=f"/channels/{self.id}", json=payload
            )
        except Exception as e:
            error = "".join(format_exception(e, e, e.__traceback__))
            log.error(f"Could not edit channel \n{error}")

    async def create_webhook(self, name: str = None, avatar_url: str = None) -> Webhook:
        """
        Creates a webhook in the specified channel

        Args:
            name (str, optional): Name of the webhook. Defaults to None.
            avatar_url (str, optional): Avatar of the webhook. Requires a URL. Defaults to None.

        Returns:
            webhook (Webhook): Returns the created webhook object.

        Raises:
            NameError: Name is required
        """
        fields = {}
        if name != None:
            fields["name"] = name
        else:
            log.error("Name is required")
        if avatar_url != None:
            data = await self.http.encode_image(avatar_url)
            fields["avatar"] = data
        data = await self.http.request(
            method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields
        )
        webhook = Webhook(data, self.bot, http=self.http)
        self.webhooks.append(webhook)
        return webhook

    async def create_invite(self, max_age: int = 0, max_uses: int = 0) -> str:
        """
        Creates an invite in the specified channel

        Args:
            max_age (int, optional) Seconds to invite expiration. Defaults to 0 (infinite).
            max_uses (int, optional) Maximum uses to invite expiration. Defaults to 0 (infinite).

        Returns:
            invite (str): Returns the channel invite link
        """
        data = await self.http.request(
            method="post",
            endpoint=f"/channels/{self.id}/invites",
            json={
                "max_age": max_age,
                "max_uses": max_uses,
                "target_type": None,
                "temporary": False,
                "flags": 0,
            },
        )
        return "https://discord.gg/" + data["code"]


class VoiceChannel(Voiceable, Messageable):
    """Voice Channel Object"""

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        super().__init__(http, bot)
        self.permissions: list[Permission] = []
        self.webhooks: list[Webhook] = []
        self.http = http
        self.bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
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
        """
        Deletes the voice channel object.
        """
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self

    async def create_webhook(self, name: str = None, avatar_url: str = None) -> Webhook:
        """
        Creates a webhook in the specified channel

        Args:
            name (str, optional): Name of the webhook. Defaults to None.
            avatar_url (str, optional): Avatar of the webhook. Requires a URL. Defaults to None.

        Returns:
            webhook (Webhook): Returns the created webhook object.

        Raises:
            NameError: Name is required
        """

        fields = {}
        if name != None:
            fields["name"] = name
        else:
            log.error("Name is required...")
        if avatar_url != None:
            data = await self.http.encode_image(avatar_url)
            fields["avatar"] = data
        data = await self.http.request(
            method="post", endpoint=f"/channels/{self.id}/webhooks", json=fields
        )
        webhook = Webhook(data, self.bot, self.http)
        self.webhooks.append(webhook)
        return webhook

    async def create_invite(self, max_age: int = 0, max_uses: int = 0) -> str:
        """
        Creates an invite in the specified channel

        Args:
            max_age (int, optional) Seconds to invite expiration. Defaults to 0 (infinite).
            max_uses (int, optional) Maximum uses to invite expiration. Defaults to 0 (infinite).

        Returns:
            invite (str): Returns the channel invite link
        """
        data = await self.http.request(
            method="post",
            endpoint=f"/channels/{self.id}/invites",
            json={
                "max_age": max_age,
                "max_uses": max_uses,
                "target_type": None,
                "temporary": False,
                "flags": 0,
            },
        )
        return "https://discord.gg/" + data["code"]


class Category:
    """Category Object"""

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        self.bot: Bot = bot
        self.http: http = http
        self.permissions: list[Permission] = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.name = data.get("name")
        self.id = data.get("id")
        self.guild_id = data.get("guild_id")
        self.position = data.get("position")
        self.flags = data.get("flags")

    async def delete(self):
        """Deletes the Category object."""
        await self.http.request(method="delete", endpoint=f"/channels/{self.id}")
        del self


class DMChannel(Voiceable, Messageable):
    """DM Channel Object"""

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        super().__init__(http, bot)
        self.http: http = http
        self.bot: Bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.recipient}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.recipient = User(data.get("recipients")[0], self.bot, self.http)
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("id")

    async def delete(self):
        """Deletes the DM Channel object."""
        await self.http.request(
            method="delete", endpoint=f"/channels/{self.id}?silent=false"
        )
        del self


class GroupChannel(Voiceable, Messageable):
    """Group Channel Object"""

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        super().__init__(http, bot)
        self.recipients = []
        self.http: http = http
        self.bot: Bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        for user in data.get("recipients"):
            self.recipients.append(User(user, self.bot, self.http))
        self.name = data.get("name")
        self.owner_id = data.get("owner_id")
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.icon = data.get("icon")

    async def delete(self):
        """Deletes the Group Channel Object"""
        await self.http.request(
            method="delete", endpoint=f"/channels/{self.id}?silent=true"
        )
        del self

    async def create_invite(self) -> str:
        """
        Creates an invite in the specified group channel

        Args:
            None

        Returns:
            invite (str): Returns the channel invite link
        """
        data = await self.http.request(
            method="post",
            endpoint=f"/channels/{self.id}/invites",
            json={"max_age": 86400},
        )
        return "https://discord.gg/" + data["code"]
