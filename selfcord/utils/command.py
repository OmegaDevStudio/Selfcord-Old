
import inspect


class Command:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.aliases = [self.name] + kwargs.get('aliases', [])
        self.description = kwargs.get('description')
        self.func = kwargs.get("func")
        self.check = inspect.signature(self.func).return_annotation
        self.signature = inspect.signature(self.func).parameters.items()

class CommandCollection:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}

    
    def __iter__(self):
        for cmd in self.commands.values():
            yield cmd

    def _is_already_registered(self, cmd):
        for command in self.commands.values():
            for alias in cmd.aliases:
                if alias in command.aliases:
                    return True

    def add(self, cmd):
        if not isinstance(cmd, Command):
            raise ValueError('cmd must be a subclass of Command')
        if self._is_already_registered(cmd):
            raise ValueError('A name or alias is already registered')
        self.commands[cmd.name] = cmd

    def get(self, alias, prefix=''):
        try:
            return self.commands[alias]
        except KeyError:
            pass
        for command in self.commands:
            if alias in command.aliases:
                return command

class Context:
    def __init__(self, bot, message, http) -> None:
        self.bot = bot
        self.message = message
        self.http = http



    @property
    def author(self):
        return self.message.author

    @property
    def guild(self):
        return self.message.guild

    @property
    def channel(self):
        return self.message.channel

    @property
    def content(self):
        return self.message.content

    @property
    def command(self):
        if self.prefix is None:
            return None
        for command in self.bot.commands:
            for alias in command.aliases:
                if self.content.startswith(self.prefix + alias):
                    return command
        return None

    @property
    def alias(self):
        for command in self.bot.commands:
            for alias in command.aliases:

                if self.content.startswith(self.prefix + alias):
                    return alias
        return None

    @property
    def prefix(self):
        for prefix in self.bot.prefixes:
            if self.content.startswith(prefix):
                return prefix

    @property
    def command_content(self):
        if self.alias == None:
            return
        try:
            cut = len(self.prefix + self.alias)
            return self.content[cut:]
        except:
            return None

    async def get_arguments(self):
        if self.command_content != None:
            splitted = self.command_content.split()
        args = splitted
        return args



    async def invoke(self):
        if self.command is None:
            return
        if self.message.author.id != self.bot.user.id:

            return
        if self.command_content != None:

            args = await self.get_arguments()
            func = self.command.func
            args.insert(0, self)

        await func(*args)






    async def send(self, content: str, tts: bool=False):
        await self.channel.send( content=content, tts=tts)





