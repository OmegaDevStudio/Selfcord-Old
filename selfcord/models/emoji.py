

class Emoji:
    """Emoji Object
    """
    def __init__(self, data, bot, http) -> None:
        self.bot = bot
        self.http = http
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
        self.guild_id = data.get("guild_id")


    async def delete(self):
        await self.http.request(method="delete", endpoint=f"/guilds/{self.guild_id}/emojis/{self.id}")
        del self
