

class Member:
    """Member Object
    """
    def __init__(self, UserPayload: dict) -> None:
        self.roles = []

        self._update(UserPayload)

    def __str__(self):
        return f"""{self.name}#{self.discriminator}"""


    def _update(self, data):
        user = data.get("user")
        self.name = user.get("username")
        self.id = user.get("id")
        self.discriminator = user.get("discriminator")
        self._avatar = user.get("avatar")
        self._banner = user.get("banner")
        self._accent_colour = user.get('accent_color')
        self._public_flags = user.get('public_flags')
        self.bot = user.get('bot')
        self.joined_at = data.get('joined_at')
        self.nick = data.get("nick")
        self.system = data.get('system')
