from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selfcord.api.http import http
    from selfcord.bot import Bot

    from .role import Role



class Member:
    """Member Object"""

    def __init__(self, UserPayload: dict, http: http, bot: Bot) -> None:
        self.roles: list[Role] = []

        self._update(UserPayload)

    def __str__(self):
        return f"""{self.name}#{self.discriminator}"""

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data: dict):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        user = data.get("user")
        self.name = user.get("username")
        self.id = user.get("id")
        self.discriminator = user.get("discriminator")
        self._avatar = user.get("avatar")
        self._banner = user.get("banner")
        self._accent_colour = user.get("accent_color")
        self._public_flags = user.get("public_flags")
        self.bot_acc = user.get("bot")
        self.joined_at = data.get("joined_at")
        self.nick = data.get("nick")
        self.system = data.get("system")

    async def create_dm(self):
        """Create a dm for the user"""
        from .channel import DMChannel
        return DMChannel(await self.http.request(
            method="post",
            endpoint="/users/@me/channels",
            json={"recipients": [self.id]},
        ), self.bot, self.http)

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
