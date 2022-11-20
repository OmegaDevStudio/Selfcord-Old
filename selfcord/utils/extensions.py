from .command import CommandCollection, Command
import inspect

class Extension:
    """Extension object pretty much
    """
    def __init__(self, **kwargs):
        self.name: str | None = kwargs.get("name")
        self.description: str | None = kwargs.get('description')
        self.ext = kwargs.get("ext")
        self.commands = self.ext.commands

class Extender:
    commands = CommandCollection()

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
            cmd = Command(name=name, description=description, aliases=aliases, func=coro)
            cls.commands.add(cmd)







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
            raise ValueError('cmd must be a subclass of Command')
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
