

from textwrap import wrap
from ..models import User
import asyncio
from aioconsole import aprint
import inspect

class EventHandler:
    def __init__(self):
        self._events = {}


    async def handle_ready(self, data):
        self.client.user = ClientUser(self.client, data)

        for guild in data['guilds']:
            await self.handle_guild_create(guild)

        for channel in data["private_channels"]:
            if channel["type"] == DMCHANNEL:
                self.client.channels.add(DMChannel(self.client, data))
            elif channel["type"] == GROUPDMCHANNEL:
                self.client.channels.add(DMGroupChannel(self.client, data))





