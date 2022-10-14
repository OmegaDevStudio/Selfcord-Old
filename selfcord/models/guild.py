from .member import Member
from .channel import TextChannel, VoiceChannel, Category
from .role import Role
from .emoji import Emoji
from itertools import zip_longest
class Guild:
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

    def __init__(self, data, http) -> None:
        self.roles = []
        self.emojis = []
        self.members = []
        self.channels = []
        self.http = http
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.region = data.get('region')
        self.splash = data.get('splash')
        self.mfa_level = data.get('mfa_level')
        self.features = data.get('features')
        self.unavailable = data.get('unavailable')
        self.verification_level = data.get('verification_level')
        self.explicit_content_filter = data.get('explicit_content_filter')
        self.owner_id = data.get('owner_id')

        for (member, channel, role, emoji) in zip_longest(data.get('members'), data.get("channels"), data.get("roles"), data.get("emojis")):
            if member != None:
                user = Member(member)
                self.members.append(user)

            if channel != None:
                type = channel.get("type")
                if type == self.TEXTCHANNEL:
                    channel = TextChannel(channel, self.http)
                    self.channels.append(channel)
                elif type == self.VOICECHANNEL:
                    channel = VoiceChannel(channel, self.http)
                    self.channels.append(channel)
                elif type == self.CATEGORY:
                    channel = Category(channel, self.http)
                    self.channels.append(channel)
                else:
                    channel = TextChannel(channel, self.http)
                    self.channels.append(channel)

            if role != None:
                role = Role(role, guild_id = self.id)
                self.roles.append(role)

            if emoji != None:
                emoji = Emoji(emoji)
                self.emojis.append(emoji)

    async def txt_channel_create(self, name):
        await self.http.request(method="post", endpoint=f"/guilds/{self.id}/channels", json={"name": f"{name}", "permission_overwrites": [], "type": 0})

    async def vc_channel_create(self, name):
        await self.http.request(method="post", endpoint=f"/guilds/{self.id}/channels", json={"name": f"{name}", "permission_overwrites": [], "type": 2})
    
    async def role_create(self, name):
        await self.http.request(method = "post", endpoint = f"/guilds/{self.id}/roles", json = {"name": f"{name}"})
        
    async def category_channel_create(self, name):
        await self.http.request(method="post", endpoint=f"/guilds/{self.id}/channels", json={"name": f"{name}", "permission_overwrites": [], "type": 4})
    

