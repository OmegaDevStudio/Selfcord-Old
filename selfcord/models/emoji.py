

class Emoji:
    def __init__(self, data) -> None:
        self._update(data)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def _update(self, data):
        self.name = data.get("name")
        self.id = data.get("id")
        self.roles = data.get("roles")
        self.managed = data.get("managed")
        self.available = data.get("available")
        self.animated = data.get("animated")

