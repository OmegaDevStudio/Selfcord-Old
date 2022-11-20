
import inspect
import re







class Command:
    """Command Object pretty much
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.aliases = [self.name] + kwargs.get('aliases', [])
        self.description = kwargs.get('description')
        self.func = kwargs.get("func")
        self.check = inspect.signature(self.func).return_annotation
        self.signature = inspect.signature(self.func).parameters.items()

class CommandCollection:
    """Commands collection, where commands are stored into
    """
    def __init__(self):
        self.commands = {}

    def __len__(self):
        return len(self.commands)
    def __iter__(self):
        for cmd in self.commands.values():
            yield cmd

    def _is_already_registered(self, cmd):
        for command in self.commands.values():
            for alias in cmd.aliases:
                if alias in command.aliases:
                    return True

    def append(self, cmd):
        if not isinstance(cmd, CommandCollection):
            raise ValueError('cmd must be a subclass of CommandCollection')
        for item in cmd:
            self.commands[item.name] = item

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
    """Context related for commands, and invokation
    """
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
        """The content minus the prefix and command name, essentially the args

        Returns:
            str: String of content
        """
        if self.alias == None:
            return
        try:
            cut = len(self.prefix + self.alias)
            return self.content[cut:]
        except:
            return None

    def get_converter(self, param):
        if param.annotation is param.empty:
            return str
        if callable(param.annotation):
            return param.annotation
        else:
            raise ValueError('Parameter annotation must be callable')

    def convert(self, param, value):
        """Attempts to turn x value in y value, using get_converter func for the values

        Args:
            param (_type_): function parameter
            value (_type_): value in message

        Returns:
            Type[str]: The type of parameter
        """
        converter = self.get_converter(param)
        return converter(value)

    async def get_arguments(self):
        """Get arguments by checking function arguments and comparing to arguments in message.

        Returns:
            _type_: _description_
        """
        args = []
        kwargs = {}

        if self.command.signature is not None:
            signature = self.command.signature
        if self.command_content != "":
            splitted = self.command_content.split(" ")[1:]

            for index, item in enumerate(splitted):
                user_regex = re.findall(r"<@[0-9]{18,19}>", item)
                if len(user_regex) > 0:
                    x = re.findall(r"[0-9]{18,19}", item)
                    if len(x) > 0:
                        val = x[0]
                        splitted[index] = val
                break
        else:
            return args, kwargs


        for index, (name, param) in enumerate(signature):
            if index == 0:
                continue

            if param.kind is param.POSITIONAL_OR_KEYWORD:

                arg = self.convert(param, splitted.pop(0))

                args.append(arg)
            if param.kind is param.VAR_KEYWORD:

                for arg in splitted:
                    arg = self.convert(param, arg)
                    args.append(arg)


            if param.kind is param.KEYWORD_ONLY:

                arg = self.convert(param, ' '.join(splitted))
                kwargs[name] = arg


        for key in kwargs.copy():
            if not kwargs[key]:
                kwargs.pop(key)

        return args, kwargs




    async def invoke(self):
        """Used to actually run the command
        """
        if self.command is None:
            return
        if self.message.author.id != self.bot.user.id:
            return
        if self.command_content != None:
            args, kwargs = await self.get_arguments()
            func = self.command.func
            args.insert(0, self)


        await func(*args, **kwargs)



    async def reply(self, content: str, tts=False):
        """Helper function to reply to your own message containing the command

        Args:
            content (str): The message you would like to send
            tts (bool, optional): Whether message should be tts or not. Defaults to False.
        """
        await self.channel.reply(self.message, content, tts)

    async def send(self, content: str, tts=False):
        """Helper function to send message to the current channel

        Args:
            content (str): The message you would like to send
            tts (bool, optional): Whether message should be tts or not. Defaults to False.
        """
        await self.channel.send( content=content, tts=tts)

    async def spam(self, amount: int, content: str):
        """Helper function to spam messages in the current channel (uses asyncio.gather !!!!)

        Args:
            amount (int): Amount of messages to spam
            content (str): The message you would like to send
        """
        await self.channel.spam(amount, content)

    async def purge(self, amount: int=None):
        """Helper function to purge messages in the current channel, uses asyncio gather.

        Args:
            amount (int): The amount of messages to purge, defaults to All.
        """
        await self.channel.purge(amount)




