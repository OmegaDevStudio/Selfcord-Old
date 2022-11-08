from .command import CommandCollection


class Extension:
    """Extension object pretty much
    """
    def __init__(self, **kwargs):
        self.name: str | None = kwargs.get("name")
        self.description: str | None = kwargs.get('description')
        self.ext = kwargs.get("ext")
        self.commands: CommandCollection | None = kwargs.get("commands")

class Extender:
    def __init__(self, bot) -> None:
        self.commands = CommandCollection(bot)
    class Extension:
        def __init_subclass__(cls, name=None, description="") -> None:
            super().__init_subclass__()
            cls.name = name
            cls.description = description




class ExtensionCollection:
    """Extension collection, where extensions are stored into
    """
    def __init__(self, bot):
        self.bot = bot
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
