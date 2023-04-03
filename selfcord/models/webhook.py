from typing import Any, Dict

from ..api.http import Http


class Webhook:
    def __init__(self, data: Dict[Any, Any], bot: Any, http: Http) -> None:
        self.http = http
        self.bot = bot
        self._update(data)

    def _update(self, data: Dict[Any, Any]) -> None:
        self.id = data.get("id")
        self.type = data.get("type")
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")
        self.name = data.get("name")
        self.avatar = data.get("avatar")
        self.token = data.get("token")
        self.application_id = data.get("application_id")
        self.webhook_url = f"https://discord.com/api/webhooks/{self.id}/{self.token}"
        self.source_guild = data.get("source_guild")
        self.source_channel = data.get("source_channel")

    async def send(self, content: str) -> None:
        """
        Sends a message from the webhook.

        Args:
            content (str): The message content

        Returns:
            No return value
        """
        await self.http.request(method="post", endpoint=f"/webhooks/{self.id}/{self.token}", json={"content": content})

    async def delete(self) -> None:
        """
        Deletes the webhook.

        Args:
            No arguments required

        Returns:
            No return value
        """
        await self.http.request(method="delete", endpoint=f"/webhooks/{self.id}/{self.token}")
