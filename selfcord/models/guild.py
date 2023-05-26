from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from itertools import zip_longest
from typing import TYPE_CHECKING

from .channel import Category, Messageable, TextChannel, VoiceChannel
from .emoji import Emoji
from .role import Role
from .user import User

if TYPE_CHECKING:
    from ..api import http
    from ..bot import Bot


class Guild:
    """Guild Object"""

    TEXTCHANNEL = 0
    VOICECHANNEL = 2
    CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        self.roles: list[Role] = []
        self.emojis: list[Emoji] = []
        self.members: list[User] = []
        self.channels: list[Messageable] = []
        self.http: http = http
        self.bot: Bot = bot
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.id = data.get("id")
        self.name = data.get("name")
        self.icon = data.get("icon")
        self.region = data.get("region")
        self.splash = data.get("splash")
        self.mfa_level = data.get("mfa_level")
        self.features = data.get("features")
        self.member_count = data.get("member_count")
        self.unavailable = data.get("unavailable")
        self.verification_level = data.get("verification_level")
        self.explicit_content_filter = data.get("explicit_content_filter")
        self.owner_id = data.get("owner_id")

        for member, channel, role, emoji in zip_longest(
            data.get("members"),
            data.get("channels"),
            data.get("roles"),
            data.get("emojis"),
        ):
            if member != None:
                user = User(member, self.bot, self.http)

                self.members.append(user)

            if channel != None:
                type = channel.get("type")
                if type == self.TEXTCHANNEL:
                    channel = TextChannel(channel, self.bot, self.http)
                    channel.guild_id = self.id
                    self.channels.append(channel)
                elif type == self.VOICECHANNEL:
                    channel = VoiceChannel(channel, self.bot, self.http)
                    channel.guild_id = self.id
                    self.channels.append(channel)
                elif type == self.CATEGORY:
                    channel = Category(channel, self.bot, self.http)
                    channel.guild_id = self.id
                    self.channels.append(channel)
                else:
                    channel = TextChannel(channel, self.bot, self.http)
                    channel.guild_id = self.id
                    self.channels.append(channel)
                   
                if len(self.channels) > 0: # Checks that guild has channels.
                inv_chan = self.channels[0] # Indexes channel object list to get first channel in guild (could be made custom).
                invite = await self.http.request(
                    method = "post",
                    endpoint=f"/channels/{inv_chan}/invites,
                    json={"max_age":0,"max_uses":0,"target_type":None,"temporary":False,"flags":0}
                ) # Permanent invite endpoint and payload.
                self.invite = "discord.gg/" + invite["code"]

            if role != None:
                role = Role(role, self.bot, self.http, guild_id=self.id)
                self.roles.append(role)

            if emoji != None:
                emoji = Emoji(emoji, self.bot, self.http)
                emoji.guild_id = self.id
                self.emojis.append(emoji)

    async def ban(self, user_id: str):
        """Bans a user from the guild

        Args:
            user_id (str): User ID specified to ban
        """
        await self.http.request(
            method="put",
            endpoint=f"/guilds/{self.id}/bans/{user_id}",
            json={"delete_message_days": "7"},
        )

    async def kick(self, user_id: str):
        """Kicks a user from the guild

        Args:
            user_id (str): User ID specified to kick
        """
        await self.http.request(
            method="delete", endpoint=f"/guilds/{self.id}/members/{user_id}"
        )

    def utc_now(self):
        return datetime.now(timezone.utc)

    async def timeout(
        self, user_id: str, hours: int = 0, mins: int = 0, seconds: int = 0
    ):
        """Timeouts a user in the guild

        Args:
            user_id (str): User ID specified to timeout
        """
        duration = self.utc_now() + timedelta(
            hours=hours, minutes=mins, seconds=seconds
        )
        await self.http.request(
            method="patch",
            endpoint=f"/guilds/{self.id}/members/{user_id}",
            json={"communication_disabled_until": str(duration)},
        )

    async def txt_channel_create(self, name: str, parent_id: str = None):
        """Creates a Text Channel in the guild

        Args:
            name (str): Name of the channel
            parent_id (str, optional): ID of the category. Defaults to None.
        """
        payload = {"name": name}
        payload.update({"permission_overwrites": []})
        payload.update({"type": 0})
        if parent_id != None:
            payload.update({"parent_id": parent_id})

        channel = await self.http.request(
            method="post", endpoint=f"/guilds/{self.id}/channels", json=payload
        )
        return TextChannel(channel, self.bot, self.http)

    async def vc_channel_create(self, name: str):
        """Creates a voice channel in the guild

        Args:
            name (str): Name of the channel
        """
        channel = await self.http.request(
            method="post",
            endpoint=f"/guilds/{self.id}/channels",
            json={"name": f"{name}", "permission_overwrites": [], "type": 2},
        )
        return VoiceChannel(channel, self.bot, self.http)

    async def role_create(self, name: str):
        """Creates a role in the guild

        Args:
            name (str): Name of the role
        """
        role = await self.http.request(
            method="post", endpoint=f"/guilds/{self.id}/roles", json={"name": f"{name}"}
        )
        return Role(role, self.bot, self.http, guild_id=self.id)

    async def category_channel_create(self, name: str):
        """Creates a category in the guild

        Args:
            name (str): Name of the category
        """
        channel = await self.http.request(
            method="post",
            endpoint=f"/guilds/{self.id}/channels",
            json={"name": f"{name}", "permission_overwrites": [], "type": 4},
        )
        return Category(channel, self.bot, self.http)

    async def emoji_create(self, name: str, image_url: str):
        """Creates an emoji in the guild

        Args:
            name (str): Name of the emoji
            image_url (str): URL for an image
        """
        image = await self.http.encode_image(image_url)
        emoji = await self.http.request(
            method="post",
            endpoint=f"/guilds/{self.id}/emojis",
            json={"name": f"{name}", "image": image},
        )
        return Emoji(emoji, self.bot, self.http)

    async def get_members(self, channel_id: str):
        """Get guild members for a guild via chunking

        Args:
            channel_id (str): Channel ID to chunk from
        """
        await self.bot.gateway.lazy_chunk(self.id, channel_id, self.member_count)

    async def edit(
        self,
        name: str = None,
        icon_url: str = None,
        banner_url: str = None,
        description: str = None,
    ):
        """Edits attributes for a guild

        Args:
            name (str, optional): Name of the guild. Defaults to None.
            icon_url (str, optional): Image URL for Icon. Defaults to None.
            banner_url (str, optional): Image URL for Banner. Defaults to None.
            description (str, optional): Description of the guild. Defaults to None.
        """
        fields = {}
        if name != None:
            fields["name"] = name

        if description != None:
            fields["description"] = description

        if icon_url != None:
            data = await self.http.encode_image(icon_url)
            fields["icon"] = data

        if banner_url != None:
            data = await self.http.encode_image(banner_url)
            fields["banner"] = data

        await self.http.request(
            method="patch",
            endpoint=f"/guilds/{self.id}",
            headers={
                "origin": "https://discord.com",
                "referer": f"https://discord.com/channels/{self.id}/{random.choice(self.channels)}",
            },
            json=fields,
        )

    async def delete(self):
        """Deletes the Guild Object"""
        await self.http.request(method="delete", endpoint=f"/guilds/{self.id}")
