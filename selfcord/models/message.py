from __future__ import annotations

import asyncio
import logging
import random
import time
import urllib
from itertools import zip_longest
from typing import TYPE_CHECKING

import aiofiles
import ujson

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot

from .user import User

log = logging.getLogger(__name__)

class Attachment:
    def __init__(self, data) -> None:
        self.proxy_url = data.get("proxy_url")
        self.url = data.get("url")
        self.name = data.get("filename")
        self.size = data.get("size")
        self.id = data.get("id")

class Button:
    def __init__(self, data: dict, message: Message, bot: Bot, http: http):
        self.bot = bot
        self.http = http
        self._update(data, message)

    def _update(self, data: dict, message: Message):
        self.type = 2
        self.style = data.get("style")
        self.url = data.get("url")
        self.custom_id = data.get("custom_id")
        self.label = data.get("label")
        self.emoji = data.get("emoji")
        self.disabled = data.get("disabled")
        self.message = message

    async def trigger(self):
        data = {
            "component_type": self.type,
            "custom_id": self.custom_id
        }
        json = {
            "application_id": self.message.author.id,
            "channel_id": self.message.channel_id,
            "data": data,
            "message_flags": 0,
            "message_id": self.message.id,
            "nonce": self.message.make_nonce,
            "session_id": self.bot.session_id,
            "type": 3,
        }
        if self.message.guild_id is not None:
            json['guild_id'] = self.message.guild_id
        json = await self.http.request("post", "/interactions", json=json)



class Action_Row:
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6 
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8

    def __init__(self, data: dict, message: Message, bot: Bot, http: http) -> None:
        self.bot = bot
        self.http = http
        self._update(data, message)

    def _update(self, data: dict, message: Message):
        self.type = 1
        self.message = message
        components = data.get("components")
        if components is not None:
            self.components = []
            for component in components:
                if component.get("type") == self.BUTTON:
                    self.components.append(Button(component, message, self.bot, self.http))
                elif component.get("type") in [self.STRING_SELECT, self.USER_SELECT, self.ROLE_SELECT, self.CHANNEL_SELECT, self.MENTIONABLE_SELECT]:
                    self.components.append(Select_Menu(component, message, self.bot, self.http))
                elif component.get("type") == self.TEXT_INPUT:
                    self.components.append(Text_Input(component, self.bot, self.http))
        else:
            self.components = []
        
class Select_Menu:
    TYPES = {
        "STRING_SELECT" : 3,
        "USER_SELECT" : 5,
        "ROLE_SELECT" : 6,
        "MENTIONABLE_SELECT" : 7,
        "CHANNEL_SELECT" : 8,
    }
    def __init__(self, data: dict, message: Message, bot: Bot, http: http) -> None:
        self._update(data, message)
    
    def _update(self, data: dict, message: Message):
        self.raw_type = data.get("type")
        self.message = message
        for key, val in self.TYPES.items():
            if self.raw_type == val:
                self.type = key
        self.custom_id = data.get("custom_id")
        if self.raw_type == 3:
            if data.get("options") is not None:
                self.options = [Select_Option(data) for data in data['options']]
        if self.raw_type == 8:
            self.channel_types = data.get("channel_types")
        self.placeholder = data.get("placeholder")
        self.min_values = data.get("min_values")
        self.max_values = data.get("max_values")
        self.disabled = data.get("disabled")

class Text_Input:
    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        self.bot = bot
        self.http = http
        self._update(data)

    def _update(self, data: dict):
        self.type = 4
        self.custom_id = data.get("custom_id")
        self.style = data.get("style")
        self.label = data.get("label")
        self.min_length = data.get("min_length")
        self.max_length = data.get("max_length")
        self.required = data.get("required")
        self.value = data.get("value")
        self.placeholder = data.get("placeholder")
        self.id = data.get("id")

    
    async def trigger(self, value: str, message: Message, comp_id: str):
        comp_id = "form_" + comp_id
        json = {"type": 5, "application_id": message.author.id, "channel_id": message.channel_id, "data": {"id": self.id, "custom_id": comp_id, "components": [{"type": 1, "components": [{"type": self.type, "custom_id":self.custom_id, "value": value,}]}]}, "session_id": self.bot.session_id, "nonce": message.make_nonce}
        if message.guild_id is not None:
            json['guild_id'] = message.guild_id
        await self.http.request("post", "/interactions", json=json)

class Select_Option:
    def __init__(self, data) -> None:
        self._update(data)

    def _update(self, data):
        self.label = data.get("label")
        self.value = data.get("value")
        self.description = data.get("description")
        self.emoji = data.get("emoji")
        self.default = data.get("default")


            

class Message:
    """Message Object"""
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6 
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8

    @property
    def make_nonce(self):
        """Generate pseudorandom number."""
        return str(random.randint(0, 100000000))

    def __init__(self, data, bot: Bot, http: http) -> None:
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
        components = data.get("components")
        self.components = []
        for component in components:
            if component.get("type") == 1:
                self.components.append(Action_Row(component, self, self.bot, self.http))
            elif component.get("type") == 2:
                self.components.append(Button(component, self, self.bot, self.http))
            elif component.get("type") in [self.STRING_SELECT, self.USER_SELECT, self.ROLE_SELECT, self.CHANNEL_SELECT, self.MENTIONABLE_SELECT]:
                self.components.append(Select_Menu(component, self, self.bot, self.http))
            elif component.get("type") == 4:
                self.components.append(Text_Input(component, self.bot, self.http))
            else:
                self.components.append(component)

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

    async def thread_create(self, name: str):
        """Create a thread for message object"""
        await self.http.request("post", f"/channels/{self.channel_id}/messages/{self.id}/threads", headers={"origin": "https://discord.com", "referer": f"https://discord.com/{self.guild_id}/self.channel_id"}, json = {"name": name, "auto_archive_duration": 4320, "location": "Message", "type": 11})

    async def delete(self):
        """Delete the Message Object"""
        await self.http.request(
            method="delete", endpoint=f"/channels/{self.channel_id}/messages/{self.id}"
        )

    
         
                
    async def edit(self, content: str, file_paths: list = [], delete_after: int | None = None) -> Message:
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
        if delete_after is not None:
            asyncio.create_task(self.channel.delayed_delete(Message(resp, self.bot, self.http), delete_after))
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

    async def report(self, breadcrumbs: list = []):
        await self.http.request(
            method="post",
            endpoint="/reporting/message",
            json={
                "version": "1.0",
                "variant": "3",
                "language": "en",
                "breadcrumbs": breadcrumbs,
                "elements": {},
                "name": "message",
                "channel_id": self.channel_id,
                "message_id": self.id
            }
        )
