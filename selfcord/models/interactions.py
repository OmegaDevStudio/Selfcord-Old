from __future__ import annotations

import random
import string
import time
from itertools import zip_longest
from typing import TYPE_CHECKING

import ujson
from aioconsole import aprint

if TYPE_CHECKING:
    from selfcord.api.http import http
    from selfcord.bot import Bot


class Search:
    """Search object returned from Application command search"""

    def __init__(
        self, application_commands: dict, prev_cursor: str, next_cursor: str
    ) -> None:
        self.commands: list[SlashCommand] = [
            SlashCommand(command) for command in application_commands
        ]
        self.prev_cursor: str = prev_cursor
        self.next_cursor: str = next_cursor


class Option:
    def __init__(self, data: dict) -> None:
        self.name = data["name"]
        self.type = data["type"]
        self.description = data["description"]
        self.options: list[Option] | None = (
            [Option(option) for option in data.get("options")]
            if data.get("options") is not None
            else None
        )
        self.required = data.get("required")
        self.raw_data = data
        self.value: str = None

    def __str__(self):
        return f"{self.name}"

    def __iter__(self):
        if self.options is not None:
            yield from self.options
        else:
            yield None


class SlashCommand:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: int = data["type"]
        self.version: str = data["version"]
        self.raw_data: str = data
        self.options: list[Option] | None = (
            [Option(option) for option in data.get("options")]
            if data.get("options") is not None
            else None
        )
        self.guild_id: str | None = data.get("guild_id")
        self.target_id: str | None = data.get("target_id")

    def __iter__(self):
        if self.options is not None:
            yield from self.options
        else:
            yield None

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id


class InteractionUtil:
    """Utility class intended for interactions"""

    def __init__(self, bot: Bot, http: http):
        self.bot: Bot = bot
        self.http: http = http

    async def interaction_search(
        self,
        query: str,
        channel_id: str,
        type: int = 1,
        cursor: str = None,
        bot_id: str = None,
        command_id: str = None,
    ) -> Search:
        """Search for interactions within a specific guild channel, you can specify certain parameters

        Args:
            query (str): Query to search for
            channel_id (str): Channel ID to search within
            type (int): Type of command to search for
            bot_id (str): Specify what bot specifically to search for
            command_id (str): Specify a command id to search for, to view options

        Returns:
            Search object
        """

        endpoint = (
            f"/channels/{channel_id}/application-commands/search?query={query}&limit=7"
        )
        endpoint += f"&type={type}"
        if cursor is not None:
            endpoint += f"&cursor={cursor}"
        if command_id is not None:
            endpoint += f"&command_id={command_id}"
        if bot_id is not None:
            endpoint += f"&application_id={bot_id}"
        data = await self.http.request("get", endpoint)
        return Search(
            data["application_commands"],
            data["cursor"]["previous"],
            data["cursor"]["next"],
        )

    async def trigger_slash(
        self,
        command: SlashCommand,
        channel_id: str,
        bot_id: str,
        value: list[str | None] | None = None,
        option: list[Option] | None = None,
        guild_id: str | None = None,
    ):
        nonce = int(time.time())
        payload = {
            "type": 2,
            "application_id": bot_id,
            "channel_id": channel_id,
            "nonce": nonce,
            "session_id": self.bot.session_id,
        }
        if guild_id is not None:
            payload["guild_id"] = guild_id
        data = {
            "version": command.version,
            "id": command.id,
            "name": command.name,
            "type": command.type,
            "options": [],
            "application_command": command.raw_data,
            "attachments": [],
        }
        if option is not None:
            dic = {"options": []}
            for index, (opt, value) in enumerate(zip_longest(option, value)):
                if index == 0:
                    if value is None:
                        dic["options"].append(
                            {"name": opt.name, "type": opt.type, "options": []}
                        )
                    else:
                        dic["options"].append(
                            {"name": opt.name, "type": opt.type, "value": value}
                        )
                elif value is not None:
                    for opten in dic["options"]:
                        opten["options"].append(
                            {"name": opt.name, "type": opt.type, "value": value}
                        )

            data |= dic
        payload["data"] = data
        randstr = "".join(random.sample(string.ascii_letters + string.digits, k=16))
        boundary_val = f"----WebkitFormBoundary{randstr}"
        req_data = f'--{boundary_val}\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{ujson.dumps(payload)}\r\n--{boundary_val}--'
        await self.http.request(
            "post",
            "/interactions",
            headers={"content-type": f"multipart/form-data; boundary={boundary_val}"},
            data=req_data,
        )
