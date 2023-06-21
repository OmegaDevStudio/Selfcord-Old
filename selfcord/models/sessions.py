from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.http import http
    from ..bot import Bot

class Event_Session:
    def __init__(self, data: dict, bot: Bot, http: http):
        self.bot = bot
        self.http = http
        self._update(data)

    def _update(self, data):
        self.id = data.get("session_id")
        self.status = data.get("status")
        info = data.get("client_info")
        self.os = info.get("os")
        self.platform = info.get("client")
        self.version = info.get("version")
        if self.id == "all":
            self.type = "presence"
        elif (self.platform == "mobile") and (self.os == "other"):
            self.type = "selfcord"
        else:
            self.type = "user"


class Session:
    def __init__(self, data: dict, bot: Bot, http: http):
        self.bot = bot
        self.http = http
        self._update(data)

    def _update(self, data):
        self.last_used: str = data.get("approx_last_used_time")
        self.hash: str = data.get("id_hash")
        info = data.get("client_info")
        self.location: str = info.get("location")
        self.os: str = info.get("os")
        self.platform: str= info.get("platform")
        
       
    async def remove(self, password):
        """
        Method to logout of a particular session

        Args:
            password: Your password
        """
        await self.http.request("post", "/auth/sessions/logout", json={"session_id_hashes": [self.hash], "password": password})
        del self
