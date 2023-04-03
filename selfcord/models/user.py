import datetime
from base64 import b64encode
from typing import Dict, Any, Optional

from ..api.http import Http


class Profile:
    def __init__(self, user_payload: Dict[Any, Any], bot: Any, http: Http) -> None:
        self.bot = bot
        self.http = http

        self.__update(user_payload)

    def __update(self, data: dict):
        self.connected_accounts = [ConnectedAccount(account) for account in data.get("connected_accounts")]

        self.mutual_guilds = [self.bot.get_guild(guild['id']) for guild in data.get("mutual_guilds")]

        self.id = data['user']['id']
        self.premium_type = data.get("premium_type")
        user_profile = data.get("user_profile")
        self.emoji = user_profile.get("emoji")
        self.bio = user_profile.get("bio")
        self.accent_color = user_profile.get("accent_color")
        self.banner = user_profile.get("banner")
        self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024" \
            if self.banner is not None else None


class ConnectedAccount:
    def __init__(self, data) -> None:
        self.__update(data)

    def __update(self, data: Dict[Any, Any]) -> None:
        self.type = data.get("type")
        self.name = data.get("name")
        self.id = data.get("id")


class User:
    """User Object
    """

    def __init__(self, user_payload: Dict[Any, Any], bot: Any, http: Http) -> None:
        self.bot = bot
        self.http = http
        self._update(user_payload)

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    @property
    def created_at(self) -> datetime.datetime:
        """
        Gets a User creation data
        """
        return datetime.datetime.utcfromtimestamp(((int(self.id) >> 22) + 1420070400000) / 1000)

    @property
    def b64token(self) -> str:
        return str(b64encode(self.id.encode("utf-8")), "utf-8")

    def _update(self, data: Dict[Any, Any]) -> None:
        self.name = data.get("username")
        self.id = data.get("id")
        self.discriminator = data.get("discriminator")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")
        self.accent_colour = data.get('accent_color')
        self.public_flags = data.get('public_flags')
        self.bot_acc = data.get('bot')
        self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=4096" \
            if self.avatar is not None else None
        self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024" \
            if self.banner is not None else None
        self.system = data.get('system')

    async def create_dm(self) -> None:
        """
        Creates a direct message channel with this user.
        """
        await self.http.request(method="post", endpoint="/users/@me/channels", json={"recipients": [self.id]})

    async def get_profile(self) -> Optional[Profile]:
        """
        Gets the user's profile

        Returns:
            Profile: The user's profile
        """
        data = await self.http.request(method="get", endpoint=f"/users/{self.id}/profile?with_mutual_guilds=true")

        if data is not None:
            data = Profile(data, self.bot, self.http)

        return data
