from time import perf_counter
from ..models.role import Role
from ..models import User, Client, Guild, TextChannel, VoiceChannel, DMChannel, GroupChannel, Message
from aioconsole import aprint


class EventHandler:
    '''
    Used to handle discord events
    '''
    def __init__(self, bot, http):
        self._events = {}
        self.http    = http
        self.bot     = bot

    async def handle_ready(self, data, user: Client, http):
        '''Handles the ready event, what is executed when it appears
        '''
        self.user = user
        for relationship in data.get('relationships'):
            if relationship.get('type') == 1:
                self.user.friends.append(User(relationship['user'], self.bot, http))

        for channel in data.get('private_channels'):
            if channel.get('type') == 1: self.user.private_channels.append(DMChannel(channel,self.bot, http))
            if channel.get('type') == 3: self.user.private_channels.append(GroupChannel(channel, self.bot, http))

        for guild in data.get('guilds'):
            await self.handle_guild_create(guild, self.user, http)

        # Sends data from ready to the event handler in main.py (if it exists)
        await self.bot.emit('ready', perf_counter() - self.bot.t1)

    async def handle_guild_create(self, data, user: Client, http):
        '''
        Handles what happens when a guild is created
        '''
        self.user = user
        guild = Guild(data, self.bot, http)
        self.user.guilds.append(guild)

        # Sends data from ready to the event handler in main.py (if it exists)
        await self.bot.emit('guild_create', guild)

    async def handle_message_create(self, data, user: Client, http):
        '''Handles what happens when a message is created
        '''
        self.user = user
        message = Message(data, self.bot, http)
        self.user.messages.append(message)

        # Sends data from ready to the event handler in main.py (if it exists)
        await self.bot.emit('message', message)
        if message.author.id == self.bot.user.id:
            for prefix in self.bot.prefixes:
                # Attempts to invoke the command if has prefix and from the user
                if message.content.startswith(prefix): await self.bot.process_commands(message)

    async def handle_message_delete(self, data, user: Client, http):
        '''Handles what happens when a message is created. Disclaimer: Only guild id, message id and channel id will be present if the message is not in bots cache.
        '''
        self.user = user
        id =data.get('id')
        for message in self.user.messages:
            if message.id == id:
                await self.bot.emit('message_delete', message)
                self.user.deleted_messages.append(message)
                self.user.messages.remove(message)
        else:
            class deleted_message:
                def __init__(self, data) -> None:
                    self.tts                = data.get('tts')
                    self.references_message = data.get('referenced_message')
                    self.mentions           = data.get('mentions')
                    self.author             = None
                    self.id                 = data.get('id')
                    self.flags              = data.get('flags')
                    self.embeds             = data.get('embeds')
                    self.content            = data.get('content')
                    self.components         = data.get('components')
                    self.channel_id         = data.get('channel_id')
                    self.attachments        = data.get('attachments')
                    self.guild_id           = data.get('guild_id')
                    self.channel            = None
                    self.guild              = None

            message = deleted_message(data)
            await self.bot.emit('message_delete', message)

    async def handle_channel_create(self, channel, user: Client, http):
        '''Handles what happens when a channel is created
        '''
        self.user = user
        if channel.get('type') == 0:
            id = channel.get('guild_id')
            for guild in self.user.guilds:
                if guild.id == id:
                    channel = TextChannel(channel, self.bot, self.http)
                    guild.channels.append(channel)

        elif channel.get('type') == 1: self.user.private_channels.append(DMChannel(channel, self.bot, http))

        elif channel.get('type') == 2:
            id = channel.get('guild_id')
            for guild in self.user.guilds:
                if guild.id == id:
                    channel = VoiceChannel(channel, self.bot, self.http)
                    guild.channels.append(channel)

        elif channel.get('type') == 3: self.user.private_channels.append(GroupChannel(channel, self.bot, http))

        else:
            id = channel.get('guild_id')
            for guild in self.user.guilds:
                if guild.id == id:
                    channel = TextChannel(channel, self.bot, self.http)
                    guild.channels.append(channel)

        # Sends data from ready to the event handler in main.py (if it exists)
        await self.bot.emit('channel_create', channel)

    async def handle_guild_member_list_update(self, data, user: Client, http):
        '''Handles what happens when member chunk payload is sent via gateway
        '''
        members   = []
        self.user = user

        try:
            for item in data['ops'][0]['items']:
                try: members.append(User(item['member']['user'], self.bot, http))
                except: continue

            await self.bot.emit('member_chunk', members)
        except: pass



    async def handle_channel_delete(self, data, user: Client, http):
        '''Handles what happens when a channel is deleted
        '''
        self.user = user
        id = data.get('id')
        for channel in self.user.private_channels:
            if channel.id == id:
                await self.bot.emit('channel_delete', channel)
                self.user.private_channels.remove(channel)
                return

        guild_id = data.get('guild_id')
        if guild_id != None:
            for guild in self.user.guilds:
                if guild_id == guild.id:
                    for channel in guild.channels:
                        if channel.id == id:
                            await self.bot.emit('channel_delete', channel)
                            guild.channels.remove(channel)
                            return
        else:
            for guild in self.user.guilds:
                for channel in guild.channels:
                    if channel.id == id:
                        await self.bot.emit('channel_delete', channel)
                        guild.channels.remove(channel)
                        return


    async def handle_guild_role_create(self, role, user: Client, http):
        '''Handles what happens when a role is created
        '''
        self.user = user

        for guild in self.user.guilds:
            if role.get('guild_id') == guild.id:
                role = Role(role, self.http, guild_id=guild.id)
                guild.roles.append(role)

        await self.bot.emit('role_create', role)

    async def handle_guild_role_delete(self, role, user: Client, http):
        '''Handles what happens when a role is deleted
        '''
        self.user = user

        for guild in self.user.guilds:
            if role.get('guild_id') == guild.id:
                for role in guild.roles:
                    if role.get('id') == role.id:
                        await self.bot.emit('role_delete', role)
                        guild.roles.remove(role)
                        return










