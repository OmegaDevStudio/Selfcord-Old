from __future__ import annotations

from typing import TYPE_CHECKING

from .permission import Permission

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot


class Role:
    """Role Object"""

    def __init__(self, data: dict, bot: Bot, http: http, **kwargs) -> None:
        self.guild_id = kwargs.get("guild_id")
        self.http: http = http
        self.bot: Bot = bot
        self._update(data)

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        role = data.get("role")

        self.id = data.get("id") if role is None else role.get("id")
        self.permissions = (
            Permission(int(data.get("permissions"))).permissions
            if role is None
            else Permission(int(role.get("permissions"))).permissions
        )
        self.name = data.get("name") if role is None else role.get("name")
        self.mentionable = (
            data.get("mentionable") if role is None else role.get("mentionable")
        )
        self.managed = data.get("managed") if role is None else role.get("managed")
        self.icon = data.get("icon") if role is None else role.get("icon")
        self.flags = data.get("flags") if role is None else role.get("flags")

        self.color = data.get("color") if role is None else role.get("color")
        self.hoist = data.get("hoist") if role is None else role.get("hoist")
        if self.guild_id is None:
            self.guild_id = data.get("guild_id")

    def __str__(self) -> str:
        return f"{self.name}"

    async def delete(self):
        """Delete the Role Object"""
        await self.http.request(
            method="delete", endpoint=f"/guilds/{self.guild_id}/roles/{self.id}"
        )
        del self
