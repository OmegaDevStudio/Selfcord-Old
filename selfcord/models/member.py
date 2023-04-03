from typing import Dict, Any


class Member:
    """Member Object"""

    def __init__(self, user_payload: Dict[Any, Any]) -> None:
        self.roles = []

        self._update(user_payload)

    def __str__(self) -> str:
        return f"{self.name!r}#{self.discriminator!r}"

    def _update(self, data: Dict[Any, Any]) -> None:
        user = data.get("user")
        self.name = user.get("username")
        self.id = user.get("id")
        self.discriminator = user.get("discriminator")
        self._avatar = user.get("avatar")
        self._banner = user.get("banner")
        self._accent_colour = user.get('accent_color')
        self._public_flags = user.get('public_flags')
        self.bot_acc = user.get('bot')
        self.joined_at = data.get('joined_at')
        self.nick = data.get("nick")
        self.system = data.get('system')
