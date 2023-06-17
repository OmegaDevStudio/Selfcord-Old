from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .channel import Voiceable
    from .guild import Guild
    from .message import Message
    from .user import User


class Client:
    """Client Object"""

    def __init__(self, UserPayload: dict) -> None:
        self.guilds: list[Guild] = []
        self.private_channels: list[Voiceable] = []
        self.friends: list[User] = []
        self.messages: list[Message] = []
        self.deleted_messages: list[Message] = []
        self._update(UserPayload)

    def __str__(self) -> str:
        return f"""{self.name}#{self.discriminator}"""

    def __eq__(self, other):
        return self.id == other.id

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

        self.bio = data.get("bio")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.accent_colour = data.get("accent_color")
        self.public_flags = data.get("public_flags")
        self.bot_acc = data.get("bot")
        self.system = data.get("system")
