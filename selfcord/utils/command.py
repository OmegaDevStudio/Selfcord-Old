
import inspect
import re
from collections import defaultdict


class Extension:
    """Extension object pretty much
    """
    def __init__(self, **kwargs):
        self.name: str | None = kwargs.get("name")
        self.description: str | None = kwargs.get('description')
        self.ext = kwargs.get("ext")
        self._events = defaultdict(list)
        _events = self.ext._events
        commands = self.ext.commands
        self.commands = CommandCollection()
        for cmd in commands.recents():
            setattr(cmd, "ext", self.ext)
            self.commands.add(cmd)
        self.commands.copy()
        commands.clear()
        self._events.update(_events)
        _events.clear()




class ExtensionCollection:
    """Extension collection, where extensions are stored into
    """
    def __init__(self):
        self.extensions = {}

    def __iter__(self):
        for cmd in self.extensions.values():
            yield cmd

    def _is_already_registered(self, ext):
        for extension in self.extensions.values():
            if ext.name == extension:
                return True

    def add(self, ext):
        if not isinstance(ext, Extension):
            raise ValueError('cmd must be a subclass of Extension')
        if self._is_already_registered(ext):
            raise ValueError('A name or alias is already registered')
        self.extensions[ext.name] = ext

    def get(self, alias, prefix=''):
        try:
            return self.extensions[alias]
        except KeyError:
            pass
        for command in self.extensions:
            if command.name in command.aliases:
                return command



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
    def __init__(self, **kwargs):
        self.commands = {}
        self.recent_commands = {}

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

    def append(self, collection):
        if not isinstance(collection, CommandCollection):
            raise ValueError('collection must be a subclass of ExtensionCollection')
        for item in collection:
            self.commands[item.name] = item
            self.recent_commands[item.name] = item

    def add(self, cmd):
        if not isinstance(cmd, Command):
            raise ValueError('cmd must be a subclass of Command')
        if self._is_already_registered(cmd):
            raise ValueError('A name or alias is already registered')
        self.commands[cmd.name] = cmd
        self.recent_commands[cmd.name] = cmd

    def recents(self):
        for cmd in self.recent_commands.values():
            yield cmd

    def copy(self):
        self.commands.update(self.recent_commands)
        self.clear()

    def clear(self):
        self.recent_commands.clear()

    def get(self, alias, prefix=''):
        try:
            return self.commands[alias]
        except KeyError:
            pass
        for command in self.commands:
            if alias in command.aliases:
                return command
class Event:
    def __init__(self, name, coro, ext) -> None:
        self.name = name
        self.coro = coro
        self.ext = ext


class Extender:
    commands = CommandCollection()
    _events = defaultdict(list)
    def __init_subclass__(cls, name=None, description="") -> None:
        super().__init_subclass__()
        cls.name = name
        cls.description = description




    @classmethod
    def cmd(cls, description="", aliases=[]):
        """Decorator to add commands for the bot

        Args:
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you suck and don't use a coroutine
        """
        if isinstance(aliases, str):
            aliases = [aliases]

        def decorator(coro):
            name = coro.__name__
            if not inspect.iscoroutinefunction(coro):
                raise RuntimeWarning("Not an async function!")
            else:
                cmd = Command(name=name, description=description, aliases=aliases, func=coro)
                cls.commands.add(cmd)

            return cmd

        return decorator

    @classmethod
    def on(cls, event: str):
        """Decorator for events

        Args:
            event (str): The event to check for
        """

        def decorator(coro):
            if not inspect.iscoroutinefunction(coro):
                raise RuntimeWarning("Faulure")
            else:
                cls._events[event].append(Event(name=event, coro=coro, ext=cls))

                def wrapper(*args, **kwargs):
                    result = cls._events[event].append(Event(name=event, coro=coro, ext=cls))
                    return result

                return wrapper
        return decorator


    @classmethod
    def add_cmd(cls, coro, description="", aliases=[]):
        """
        Function to add commands manually without decorator

        Args:
            coro (coroutine): The function to add
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you suck and don't use a coroutine
        """
        if isinstance(aliases, str):
            aliases = [aliases]
        name = coro.__name__
        if not inspect.iscoroutinefunction(coro):
            raise RuntimeWarning("Not an async function!")
        else:


            cmd = Command(name=name, description=description, aliases=aliases, func=coro, ext=cls)
            cls.commands.add(cmd)
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
                if self.content.lower().startswith(self.prefix + alias):
                    return command
        for extension in self.bot.extensions:

            for command in extension.commands:

                for alias in command.aliases:

                    if self.content.startswith(self.prefix + alias):

                        self.extension = extension.ext
                        return command
        return None

    @property
    def alias(self):
        for command in self.bot.commands:
            for alias in command.aliases:
                if self.content.startswith(self.prefix + alias):
                    return alias
        for extension in self.bot.extensions:
            for command in extension.commands:
                for alias in command.aliases:
                    if self.content.startswith(self.prefix + alias):
                        self.extension = extension.ext
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
            if name == "ctx" or name == "self":
                continue


            if param.kind is param.POSITIONAL_OR_KEYWORD:
                try:

                    arg = self.convert(param, splitted.pop(0))
                    args.append(arg)
                except:
                    pass
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
            if func.__code__.co_varnames[0] == "self":

                args.insert(0, self.extension)
                args.insert(1, self)
            else:

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




