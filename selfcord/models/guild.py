from .member import Member
from .channel import TextChannel, VoiceChannel, Category
from .role import Role
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

        for member in data.get('members'):
            user = Member(member)
            self.members.append(user)
        for channel in data.get("channels"):
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
        for role in data.get("roles"):
            role = Role(role)
            self.channels.append(role)




