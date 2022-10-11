from time import perf_counter
from ..models import User, Client, Guild, DMChannel, GroupChannel, Message
from aioconsole import aprint


class EventHandler:
    def __init__(self, bot, http):
        self._events = {}
        self.http = http
        self.bot = bot

    async def handle_ready(self, data, user: Client, http):
        t1 = perf_counter()
        self.user = user
        for relationship in data.get("relationships"):
            if relationship.get("type") == 1:
                self.user.friends.append(User(relationship["user"]))

        for channel in data.get("private_channels"):
            if channel.get("type") == 1:
                self.user.private_channels.append(DMChannel(channel, http))
            if channel.get("type") == 3:
                self.user.private_channels.append(GroupChannel(channel, http))
        for guild in data.get("guilds"):
            await self.handle_guild_create(guild, self.user, http)
        await self.bot.emit("ready", perf_counter() - t1)


    async def handle_guild_create(self, data, user: Client, http):
        self.user = user
        guild = Guild(data, http)
        self.user.guilds.append(guild)
        await self.bot.emit("guild_create", guild)

    async def handle_message_create(self, data, user: Client, http):
        self.user = user
        message = Message(data, self.bot, http)
        self.user.messages.append(message)
        await self.bot.emit("message_create", message)
        if message.author.id == self.bot.user.id:
            for prefix in self.bot.prefixes:
                if message.content.startswith(prefix):
                    await self.bot.process_commands(message)












