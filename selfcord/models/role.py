from .permission import Permission

class Role:
    def __init__(self, data: dict) -> None:
        self._update(data)

    def _update(self, data):
        self.id = data.get("id")

        self.permissions = Permission(int(data.get("permissions"))).permissions
        self.name = data.get("name")
        self.mentionable = data.get("mentionable")
        self.managed = data.get("managed")
        self.icon = data.get("icon")
        self.flags = data.get("flags")
        self.color = data.get("color")
        self.hoist = data.get("hoist")

    def __str__(self) -> str:
        return f"{self.name}"