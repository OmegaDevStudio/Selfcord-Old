class webhook:
    def __init__(self, data: dict, **kwargs) -> None:
        self.guild_id = kwargs.get("guild_id")
        self.channel_id = kwargs.get("channel_id")
        self._update(data)

    def _update(self, data):
        webhook = data.get("webhook")
        self.id = data.get("id")
        self.type = data.get("type")
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")
        self.name = data.get("name")
        self.avatar = data.get("avatar")
        self.token = data.get("token")
        self.application_id = data.get("application_id")
        self.webhook_url = f"https://discord.com/api/webhooks/{self.id}/{self.token}"

    async def send(self, content):
        await self.http.request(method = "post", endpoint = f"/webhooks/{self.id}/{self.token}", json = {"content": content})

    async def create(self, name):
        await self.http.request(method = "post", endpoint = f"/channels/{self.channel_id}/webhooks", json = {"name": name})

    async def delete(self):
        await self.http.request(method = "delete", endpoint = f"/webhooks/{self.id}/{self.token}")
