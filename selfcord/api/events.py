from time import perf_counter
from ..models import User, Client, Guild, DMChannel, GroupChannel, Message
from aioconsole import aprint


class EventHandler:
    def __init__(self, bot):
        self._events = {}
        self.bot = bot

    async def handle_ready(self, data, user: Client):
        t1 = perf_counter()
        self.user = user
        for relationship in data.get("relationships"):
            if relationship.get("type") == 1:
                self.user.friends.append(User(relationship["user"]))

        for channel in data.get("private_channels"):
            if channel.get("type") == 1:
                self.user.private_channels.append(DMChannel(channel))
            if channel.get("type") == 3:
                self.user.private_channels.append(GroupChannel(channel))
        for guild in data.get("guilds"):
            await self.handle_guild_create(guild, self.user)
        await self.bot.emit("ready", perf_counter() - t1)


    async def handle_guild_create(self, data, user: Client):
        self.user = user
        guild = Guild(data)
        self.user.guilds.append(guild)
        await self.bot.emit("guild_create", guild)

    async def handle_message_create(self, data, user: Client):
        self.user = user
        message = Message(data, self.bot)
        self.user.messages.append(message)
        await self.bot.emit("message_create", message)











