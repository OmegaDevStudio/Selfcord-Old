

class Client:
    """Client Object
    """
    def __init__(self, UserPayload: dict) -> None:

        self.guilds = []
        self.private_channels = []
        self.friends = []
        self.messages = []
        self.deleted_messages = []
        self._update(UserPayload)

    def __str__(self):
        return f"""{self.name}#{self.discriminator}"""


    def _update(self, data):
        self.name = data.get("username")
        self.id = data.get("id")
        self.discriminator = data.get("discriminator")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")
        self.bio = data.get("bio")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.accent_colour = data.get('accent_color')
        self.public_flags = data.get('public_flags')
        self.bot = data.get('bot')
        self.system = data.get('system')


