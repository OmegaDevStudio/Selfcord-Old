

from textwrap import wrap
from ..models import User, Client, Guild, DMChannel, GroupChannel
import asyncio
from aioconsole import aprint
import inspect


class EventHandler:
    def __init__(self):
        self._events = {}

    async def handle_ready(self, data, user: Client):
        self.user = user
        for relationship in data.get("relationships"):
            if relationship.get("type") == 1:
                self.user.friends.append(User(relationship["user"]))

        for channel in data.get("private_channels"):
            if channel.get("type") == 1:
                self.user.private_channels.append(DMChannel(channel))
            if channel.get("type") == 3:
                self.user.private_channels.append(GroupChannel(channel))

        await self.handle_guild_create(data, self.user)

    async def handle_guild_create(self, data, user: Client):
        self.user = user
        for guild in data.get("guilds"):
            guild = Guild(guild)
            self.user.guilds.append(guild)









