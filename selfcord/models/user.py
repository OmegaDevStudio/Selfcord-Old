from __future__ import annotations

import datetime
from base64 import b64encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot

class UserFlags:
    FLAGS = {
        "staff" : 1,
        "partner" : 2,
        "hypesquad" : 4,
        "bug_hunter" : 8,
        "mfa_sms" : 16,
        "premium_promo_dismissed" : 32,
        "hypesquad_bravery" : 64,
        "hypesquad_brilliance" : 128,
        "hypesquad_balance" : 256,
        "early_supporter" : 512,
        "team_user" : 1024,
        "system" : 4096,
        "has_unread_urgent_messages" : 8192,
        "bug_hunter_level_2" : 16384,
        "verified_bot" : 65536,
        "verified_bot_developer" : 131072,
        "discord_certified_moderator" : 262144,
        "bot_http_interactions" : 524288,
        "spammer" : 1048576,
        "disabled_nitro" : 2097152,
        "active_developer" : 4194304,
        "higher_ratelimits" : 8589934592,
        "deleted" : 17179869184,
        "deleted_sus_activity" : 34359738368,
        "self_deleted" : 68719476736,
        "premium_discriminator" : 137438953472,
        "used_desktop_client" : 274877906944,
        "used_web_client" : 549755813888,
        "used_mobile_client" : 1099511627776,
        "disabled" : 2199023255552,
        "verified" : 8796093022208,
        "quarantined" : 17592186044416,
        "collaborator_staff" : 1125899906842624,
        "restricted_collaborator" : 2251799813685248,
    }

    @classmethod
    def calculate_flags(cls, flag_value: int):
        return [
            key
            for key, value in cls.FLAGS.items()
            if (flag_value & value) == value
        ]

class Profile:
    def __init__(self, UserPayload: dict, bot: Bot, http: http) -> None:
        self.bot: Bot = bot
        self.http: http = http

        self.__update(UserPayload)

    def __update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """

        self.connected_accounts = [
            Connected_Account(account) for account in data.get("connected_accounts")
        ]

        self.mutual_guilds = [
            self.bot.get_guild(guild["id"]) for guild in data.get("mutual_guilds")
        ]

        
        self.id = data["user"]["id"]
        self.premium_type = data.get("premium_type")
        user_profile = data.get("user_profile")
        try:
            self.emoji = user_profile.get("emoji")
        except:
            self.emoji = None
        try:
            self.bio = user_profile.get("bio")
        except:
            self.bio = None
        try:
            self.accent_color = user_profile.get("accent_color")
        except:
            self.accent_color = None
        try:
            self.banner = user_profile.get("banner")
        except:
            self.banner = None
        self.banner_url = (
            f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024"
            if self.banner != None
            else None
        )


class Connected_Account:
    def __init__(self, data) -> None:
        self.__update(data)

    def __update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.type = data.get("type")
        self.name = data.get("name")
        self.id = data.get("id")


class User:
    """User Object"""

    def __init__(self, UserPayload: dict, bot: Bot, http: http) -> None:
        self.bot: Bot = bot

        self.http: http = http
        self._update(UserPayload)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"""{self.name}#{self.discriminator}"""

    @property
    def created_at(self) -> datetime.datetime:
        """Returns the time in which the User was created

        Returns:
            datetime.datetime: The timestamp
        """
        return datetime.datetime.utcfromtimestamp(
            ((int(self.id) >> 22) + 1420070400000) / 1000
        )

    @property
    def b64token(self) -> str:
        """Returns the b64 user id

        Returns:
            str: The b64 user id
        """
        return str(b64encode(self.id.encode("utf-8")), "utf-8")

    @property
    def flags(self) -> list[str]:
        """Returns the flags of the user as a string
        
        Returns:
            list[str]: The flags
        """
        return UserFlags.calculate_flags(self.raw_flags)

    @property
    def public_flags(self) -> list[str]:
        """Returns the public flags of the user as a string
        
        Returns:
            list[str]: The flags
        """
        return UserFlags.calculate_flags(self.raw_public_flags)

    def _update(self, data):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.name = data.get("username")
        self.id = data.get("id")
        self.discriminator = data.get("discriminator")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")
        self.accent_colour = data.get("accent_color")
        self.bot_acc = data.get("bot")

        if self.avatar is not None:
            if self.avatar.startswith("a_"):
                self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.gif?size=4096"
            else:
                self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=4096"
        else:
            self.avatar_url = None

        if self.banner is not None:
            if self.banner.startswith("a_"):
                self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.gif?size=4096"
            else:
                self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=4096"
        else:
            self.banner_url = None
        self.system = data.get("system")
        self.raw_flags = data.get("flags") if data.get("flags") is not None else 0
        self.raw_public_flags = data.get("public_flags") if data.get("public_flags") is not None else 0

    async def create_dm(self):
        """Create a dm for the user"""
        await self.http.request(
            method="post",
            endpoint="/users/@me/channels",
            json={"recipients": [self.id]},
        )

    async def get_profile(self) -> Profile:
        """Get the User profile

        Returns:
            Profile: The User Profile object
        """
        data = await self.http.request(
            method="get", endpoint=f"/users/{self.id}/profile?with_mutual_guilds=true"
        )

        if data != None:
            data = Profile(data, self.bot, self.http)

        return data

    async def get_mutual_friends(self) -> list[User]:
        """Get the User mutual friends

        Returns:
            list[User]: Mutual friends
        """
        data = await self.http.request(
            method="get", endpoint=f"/users/{self.id}/relationships"
        )

        if len(data) != 0:
            return [User(user, self.bot, self.http) for user in data]
        else:
            return []
