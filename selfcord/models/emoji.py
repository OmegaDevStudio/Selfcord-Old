from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot


class Emoji:
    """Emoji Object"""

    def __init__(self, data: dict, bot: Bot, http: http) -> None:
        self.bot: Bot = bot
        self.http: http = http
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
        self.roles = data.get("roles")
        self.managed = data.get("managed")
        self.available = data.get("available")
        self.animated = data.get("animated")
        self.guild_id = data.get("guild_id")

    async def delete(self):
        """Deletes the Emoji Object"""
        await self.http.request(
            method="delete", endpoint=f"/guilds/{self.guild_id}/emojis/{self.id}"
        )
        del self
