from .user import User

class TextChannel:
    def __init__(self, data) -> None:
        self.permissions = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.topic = data.get("topic")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.name = data.get("name")
        self.id = data.get("id")
        self.last_message_id= data.get("last_message_id")
        self.flags = data.get("flags")
        self.default_thread_rate_limit_per_user = data.get("default_thread_rate_limit_per_user")
        self.category_id = data.get("parent_id")


class VoiceChannel:
    def __init__(self, data) -> None:
        self.permissions = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.name = data.get("name")
        self.id = data.get("id")
        self.last_message_id = data.get("last_message_id")
        self.rtc_region = data.get("rtc_region")
        self.flags = data.get("flags")
        self.bitrate = data.get("bitrate")
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.position = data.get("position")
        self.category_id = data.get("parent_id")

class Category:
    def __init__(self, data) -> None:
        self.permissions = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        self.name = data.get("name")
        self.id = data.get("id")
        self.position = data.get("position")
        self.flags = data.get("flags")

class DMChannel:
    def __init__(self, data) -> None:
        self._update(data)

    def __str__(self) -> str:
        return f"{self.recipient}"

    def _update(self, data):
        self.recipient = User(data.get("recipients")[0])
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("id")


class GroupChannel:
    def __init__(self, data) -> None:
        self.recipients = []
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"

    def _update(self, data):
        for user in data.get("recipients"):
            self.recipients.append(User(user))
        self.name = data.get("name")
        self.owner_id = data.get("owner_id")
        self.last_message_id = data.get("last_message_id")
        self.id = data.get("id")
        self.flags = data.get("flags")
        self.icon = data.get("icon")


