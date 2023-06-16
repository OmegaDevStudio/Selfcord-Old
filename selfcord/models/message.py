from __future__ import annotations

import asyncio
import time
import urllib
from itertools import zip_longest

from .user import User


class Attachment:
    def __init__(self, data) -> None:
        self.proxy_url = data.get("proxy_url")
        self.url = data.get("url")
        self.name = data.get("filename")
        self.size = data.get("size")
        self.id = data.get("id")


class Message:
    """Message Object"""

    def __init__(self, data, bot, http) -> None:
        self.bot = bot
        self.channel = None
        self.guild = None
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.content}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.tts = data.get("tts")
        self.referenced_message = data.get("referenced_message")
        self.author = User(data.get("author"), self.bot, self.http)
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.embeds = data.get("embeds")
        self.content = data.get("content")
        self.components = data.get("components")
        self.timestamp = time.time()
        self.channel_id = data.get("channel_id")

        attachments = data.get("attachments")
        self.attachments = []
        self.mentions = []
        for mention, atch in zip_longest(data.get("mentions"), attachments):
            if atch is not None:
                self.attachments.append(Attachment(atch))
            if mention is not None:
                self.mentions.append(User(mention, self.bot, self.http))
        self.guild_id = data.get("guild_id")

        self.channel = self.bot.get_channel(self.channel_id)

        self.guild = self.bot.get_guild(self.guild_id)

    async def delete(self):
        """Delete the Message Object"""
        await self.http.request(
            method="delete", endpoint=f"/channels/{self.channel_id}/messages/{self.id}"
        )

    async def edit(self, content: str, file_paths: list[str] = []) -> Message:
        """Edits the specified message

        Args:
            content (str): Content to edit message to.
        """
        json = { "content":  content }
        if file_paths != []:
            vals = await self.channel.upload_image(file_paths)
            json |= {"attachments" : vals}

        if self.guild_id is None:
            resp = await self.http.request(
                method="patch",
                endpoint=f"/channels/{self.channel_id}/messages/{self.id}",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.channel_id}",
                },
                json=json,
            )
        else:
            resp = await self.http.request(
                method="patch",
                endpoint=f"/channels/{self.channel_id}/messages/{self.id}",
                headers={
                    "origin": "https://discord.com",
                    "referer": f"https://discord.com/channels/{self.channel_id}/{self.guild_id}",
                },
                json=json,
            )
            resp.update({"guild_id": self.guild_id})
        return Message(resp, self.bot, self.http)

    async def react(self, emoji: str):
        """React to a message with an emoji

        Args:
            emoji (str): The emoji
        """
        raw_reaction = urllib.parse.urlencode({"emoji": emoji}).split("emoji=")[1]
        await self.http.request(
            method="put",
            endpoint=f"/channels/{self.channel_id}/messages/{self.id}/reactions/{raw_reaction}/%40me?location=Message&burst=false",
            headers={"referer": f"https://discord.com/channels/@me/{self.channel_id}"},
        )
