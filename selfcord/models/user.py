
from base64 import b64encode
import datetime


class Profile:
    def __init__(self, UserPayload: dict, bot, http) -> None:
        self.bot = bot
        self.http = http

        self.__update(UserPayload)



    def __update(self, data: dict):

        self.connected_accounts = [Connected_Account(account) for account in data.get("connected_accounts")]


        self.mutual_guilds = [self.bot.get_guild(guild['id']) for guild in data.get("mutual_guilds")]

        self.id = data['user']['id']
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
        self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024" if self.banner!=None else None

class Connected_Account:
    def __init__(self, data) -> None:
        self.__update(data)

    def __update(self, data: dict):
        self.type = data.get("type")
        self.name = data.get("name")
        self.id = data.get("id")


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
        self.bot_acc = data.get('bot')
        self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=4096" if self.avatar!=None else None
        self.banner_url = f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=1024" if self.banner!=None else None
        self.system = data.get('system')


    async def create_dm(self):
        await self.http.request(method="post", endpoint="/users/@me/channels", json={"recipients": [self.id]})

    async def get_profile(self):
        data = await self.http.request(method="get", endpoint=f"/users/{self.id}/profile?with_mutual_guilds=true")

        if data != None:
            data = Profile(data, self.bot, self.http)

        return data
