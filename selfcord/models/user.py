
from base64 import b64encode
import datetime

class User:
    """User Object
    """
    def __init__(self, UserPayload: dict, bot, http) -> None:
        self.bot = bot
        self.http = http
        self._update(UserPayload)

    def __str__(self):
        return f"""{self.name}#{self.discriminator}"""

    @property
    def created_at(self):
        return datetime.datetime.utcfromtimestamp(((int(self.id) >> 22) + 1420070400000) / 1000)

    @property
    def b64token(self):
        return str(b64encode(self.id.encode("utf-8")), "utf-8")

    def _update(self, data):
        self.name = data.get("username")
        self.id = data.get("id")
        self.discriminator = data.get("discriminator")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")
        self.accent_colour = data.get('accent_color')
        self.public_flags = data.get('public_flags')
        self.bot = data.get('bot')
        self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=4096" if self.avatar!=None else None
        self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024" if self.banner!=None else None
        self.system = data.get('system')


    async def create_dm(self):
        await self.http.request(method="post", endpoint="/users/@me/channels", json={"recipients": [self.id]})


