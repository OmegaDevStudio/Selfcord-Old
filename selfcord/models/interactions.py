from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selfcord.api.http import http
    from selfcord.bot import Bot


class Search:
    def __init__(
        self, application_commands: dict, prev_cursor: str, next_cursor: str
    ) -> None:
        self.commands = application_commands
        self.prev_cursor = prev_cursor
        self.next_cursor = next_cursor


class SlashCommand:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: int = data["type"]
        self.options: list[SlashCommand] = data.get("options")
        self.guild_id = data.get("guild_id")
        self.target_id = data.get("target_id")


class InteractionUtil:
    """Utility class intended for interactions"""

    def __init__(self, bot: Bot, http: http):
        self.bot = bot
        self.http = http

    async def interaction_search(
        self,
        query: str,
        type: int,
        channel_id: str,
        bot_id: str = None,
        command_id: str = None,
    ):
        endpoint = f"/channels/{channel_id}/application-commands/search?type={type}&query={query}&limit=7"
        if command_id is not None:
            endpoint += f"&command_id={command_id}"
        if bot_id is not None:
            endpoint += f"&application_id={bot_id}"
        await self.http.request("get", endpoint)


class Interaction:
    """Base interaction class to trigger and manipulate slash commands"""

    def __init__(self, bot: Bot, http: http):
        self.bot = bot
        self.http = http
