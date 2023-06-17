from __future__ import annotations


class Webhook:
    def __init__(self, data: dict, bot, http) -> None:
        self.http = http
        self.bot = bot
        self._update(data)

    def __eq__(self, other):
        return self.id == other.id

    def _update(self, data):
        """Updater method intended to create the attributes for the object

        Args:
            data (dict): JSON data from gateway
        """
        self.id = data.get("id")
        self.type = data.get("type")
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")
        self.name = data.get("name")
        self.avatar = data.get("avatar")

        if self.avatar is not None:
            if self.avatar.startswith("a_"):
                self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.gif?size=4096"
            else:
                self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=4096"
        else:
            self.avatar_url = None

        self.token = data.get("token")
        self.application_id = data.get("application_id")
        self.webhook_url = f"https://discord.com/api/webhooks/{self.id}/{self.token}"
        self.source_guild = data.get("source_guild")
        self.source_channel = data.get("source_channel")

    async def send(self, content: str):
        """Send a message via the webhook

        Args:
            content (str): Content of the message to send
        """
        await self.http.request(
            method="post",
            endpoint=f"/webhooks/{self.id}/{self.token}",
            json={"content": content},
        )

    async def delete(self):
        """Deletes the webhook object"""
        await self.http.request(
            method="delete", endpoint=f"/webhooks/{self.id}/{self.token}"
        )
