import inspect
import re
from collections import defaultdict
from typing import Optional, Any, Generator, List


class Extension:
    """Extension object pretty much"""

    def __init__(self, **kwargs) -> None:
        self.name: Optional[str] = kwargs.get("name")
        self.description: Optional[str] = kwargs.get('description')
        self.ext: Any = kwargs.get("ext")
        self._events: Any = kwargs.get("_events")
        commands: Any = self.ext.commands
        self.commands = CommandCollection()
        for cmd in commands.recents():
            setattr(cmd, "ext", self.ext)
            self.commands.add(cmd)
        self.commands.copy()


class ExtensionCollection:
    """Extension collection, where extensions are stored into
    """

    def __init__(self):
        self.extensions = {}

    def __iter__(self) -> Generator[Extension, None, None]:
        for cmd in self.extensions.values():
            yield cmd

    def _is_already_registered(self, ext) -> bool:
        for extension in self.extensions.values():
            if ext.name == extension:
                return True

        return False

    def add(self, ext: Any) -> None:
        if not isinstance(ext, Extension):
            raise ValueError('cmd must be a subclass of Command')
        if self._is_already_registered(ext):
            raise ValueError('A name or alias is already registered')
        self.extensions[ext.name] = ext

    def get(self, alias: Any, prefix='') -> Optional[Extension]:
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

    def __init__(self, **kwargs) -> None:
        self.name: Optional[str] = kwargs.get("name")
        self.aliases: Optional[List[Any]] = [self.name] + kwargs.get('aliases', [])
        self.description: Optional[str] = kwargs.get('description')
        self.func: Any = kwargs.get("func")
        self.check: inspect.Signature = inspect.signature(self.func).return_annotation
        self.signature: Any = inspect.signature(self.func).parameters.items()


class CommandCollection:
    """Commands collection, where commands are stored into
    """

    def __init__(self, **kwargs) -> None:
        self.commands = {}
        self.recent_commands = {}

    def __len__(self) -> int:
        return len(self.commands)

    def __iter__(self) -> Generator[Command, None, None]:
        for cmd in self.commands.values():
            yield cmd

    def _is_already_registered(self, cmd: Command) -> bool:
        for command in self.commands.values():
            for alias in cmd.aliases:
                if alias in command.aliases:
                    return True

        return False

    def append(self, collection: Any) -> None:
        if not isinstance(collection, CommandCollection):
            raise ValueError('collection must be a subclass of ExtensionCollection')
        for item in collection:
            self.commands[item.name] = item
            self.recent_commands[item.name] = item

    def add(self, cmd: Command) -> None:
        if not isinstance(cmd, Command):
            raise ValueError('cmd must be a subclass of Command')
        if self._is_already_registered(cmd):
            raise ValueError('A name or alias is already registered')
        self.commands[cmd.name] = cmd
        self.recent_commands[cmd.name] = cmd

    def recents(self) -> Generator[Command, None, None]:
        for cmd in self.recent_commands.values():
            yield cmd

    def copy(self) -> None:
        self.commands.update(self.recent_commands)
        self.recent_commands = {}

    def get(self, alias: Any, prefix='') -> Optional[Command]:
        try:
            return self.commands[alias]
        except KeyError:
            pass
        for command in self.commands:
            if alias in command.aliases:
                return command


class Event:
    def __init__(self, name: str, coro: Any, ext: Any) -> None:
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
    def cmd(cls, description: str = "", aliases: Any = None) -> Any:
        """Decorator to add commands for the bot

        Args:
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you suck and don't use a coroutine
        """
        if aliases is None:
            aliases = []

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
    def on(cls, event: str) -> Any:
        """Decorator for events

        Args:
            event (str): The event to check for
        """

        def decorator(coro) -> Any:
            if not inspect.iscoroutinefunction(coro):
                raise RuntimeWarning("Failure")
            else:
                cls._events[event].append(Event(name=event, coro=coro, ext=cls))

                def wrapper() -> Any:
                    result = cls._events[event].append(Event(name=event, coro=coro, ext=cls))
                    return result

                return wrapper

        return decorator

    @classmethod
    def add_cmd(cls, coro, description: str = "", aliases: Any = None) -> None:
        """
        Function to add commands manually without decorator

        Args:
            coro (coroutine): The function to add
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you don't use a coroutine
        """
        if aliases is None:
            aliases = []

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
        self.extension = None
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
        if self.alias is None:
            return
        try:
            cut = len(self.prefix + self.alias)
            return self.content[cut:]
        except (IndexError, ValueError, KeyError):
            return None

    @staticmethod
    def get_converter(param) -> Any:
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

    async def get_arguments(self) -> Any:
        """Get arguments by checking function arguments and comparing to arguments in message.

        Returns:
            _type_: _description_
        """
        global signature
        args_ = []
        kwargs_ = {}

        if self.command.signature is not None:
            signature = self.command.signature
        if self.command_content != "":
            split_ = self.command_content.split(" ")[1:]

            for index, item in enumerate(split_):
                user_regex = re.findall(r"<@[0-9]{18,19}>", item)
                if len(user_regex) > 0:
                    x = re.findall(r"[0-9]{18,19}", item)
                    if len(x) > 0:
                        val = x[0]
                        split_[index] = val
                break
        else:
            return args_, kwargs_

        for index, (name, param) in enumerate(signature):
            if name == "ctx" or name == "self":
                continue

            if param.kind is param.POSITIONAL_OR_KEYWORD:
                try:
                    arg = self.convert(param, split_.pop(0))
                    args_.append(arg)
                except (IndexError, ValueError, KeyError, AttributeError):
                    pass
            if param.kind is param.VAR_KEYWORD:

                for arg in split_:
                    arg = self.convert(param, arg)
                    args_.append(arg)

            if param.kind is param.KEYWORD_ONLY:
                arg = self.convert(param, ' '.join(split_))
                kwargs_[name] = arg

        for key in kwargs_.copy():
            if not kwargs_[key]:
                kwargs_.pop(key)

        return args_, kwargs_

    async def invoke(self):
        """Used to actually run the command
        """
        global func, args, kwargs
        if self.command is None:
            return
        if self.message.author.id != self.bot.user.id:
            return
        if self.command_content is not None:
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
        await self.channel.send(content=content, tts=tts)

    async def spam(self, amount: int, content: str):
        """Helper function to spam messages in the current channel (uses asyncio.gather !!!!)

        Args:
            amount (int): Amount of messages to spam
            content (str): The message you would like to send
        """
        await self.channel.spam(amount, content)

    async def purge(self, amount: int = None):
        """Helper function to purge messages in the current channel, uses asyncio gather.

        Args:
            amount (int): The amount of messages to purge, defaults to All.
        """
        await self.channel.purge(amount)
