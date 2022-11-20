import asyncio
import json
from .api import gateway, http, Activity
import inspect
from .models import Client, TextChannel, GroupChannel, DMChannel, VoiceChannel, Guild, User
from collections import defaultdict
from aioconsole import aprint, aexec
import time
from .utils import Command, CommandCollection, Context, ExtensionCollection, Extension
import random
import contextlib
from traceback import format_exception
import io
import importlib


class Bot:
    def __init__(self, show_beat: bool = False, prefixes: list = ["s!"], inbuilt_help=True) -> None:
        self.inbuilt_help= inbuilt_help
        self.show_beat = show_beat
        self.token = None
        self.http = http()
        self.t1 = time.perf_counter()
        self.gateway = gateway(self.http, self.show_beat)
        self._events = defaultdict(list)
        self.commands = CommandCollection()
        self.prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        self.extensions = ExtensionCollection()
        self.user = None

    def run(self, token: str):
        """Used to start connection to gateway as well as gather user information

        Args:
            token (str): _description_
        """
        self.token = token

        async def runner():
            data = await self.http.static_login(token)
            self.user = Client(data)
            await self.gateway.start(token, self.user, self)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    @property
    def latency(self):
        """Latency of heartbeat ack, gateway latency essentially"""
        return self.gateway.latency

    # For events
    async def inbuilt_commands(self):
        """
        I call this on bot initialisation, it's the inbuilt help command
        """
        if self.inbuilt_help:
            @self.cmd("The help command!", aliases=["test"])
            async def help(ctx, cat=None):
                if cat is None:
                    msg = f"```diff\n"
                    msg += f"+ {self.user} selfbot\n+ Prefixes:   {self.prefixes}\n\n"
                    msg += f"- Commands\n"
                    for ext in self.extensions:
                        msg += f"- Ext {ext.name}: {ext.description}\n"
                    for command in self.commands:
                        msg += f"- {command.name}:    {command.description}\n"

                        if len(msg) > 1980:
                            msg += f"```"
                    msg += f"```"
                    return await ctx.reply(f"{msg}")

                else:
                    name = cat.lower()
                    await aprint(name)
                    for ext in self.extensions:
                        if name == ext.name.lower():
                            msg = f"```diff\n"
                            msg += f"+ {self.user} selfbot\n+ Prefixes:   {self.prefixes}\n\n"
                            msg += f"- {ext.name} Commands\n"

                            for command in ext.commands:
                                msg += f"- {command.name}:    {command.description}\n"
                            msg += f"```"
                            return await ctx.reply(f"{msg}")





        def clean_code(content):
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:])[:-3]
            else:
                return content

        @self.cmd(description="Evaluates and runs code", aliases=['exec'])
        async def eval(ctx, *, code: str):
            code = clean_code(code)

            try:
                with contextlib.redirect_stdout(io.StringIO()) as f:
                    await aexec(code)
                    result = f"```{f.getvalue()}\n```"
            except Exception as e:
                error = "".join(format_exception(e, e, e.__traceback__))
                result = f"```\n{error}```"

            await ctx.reply(result)

    def on(self, event: str):
        """Decorator for events

        Args:
            event (str): The event to check for
        """

        def decorator(coro):
            if not inspect.iscoroutinefunction(coro):
                raise RuntimeWarning("Faulure")
            else:
                self._events[event].append(coro)

                def wrapper(*args, **kwargs):
                    result = self._events[event].append(coro)
                    return result

                return wrapper

        return decorator

    async def emit(self, event, *args, **kwargs):
        """Used to essentially push values to the decorator

        Args:
            event (str): The event name
        """
        on_event = "on_{}".format(event)
        try:
            if hasattr(self, on_event):
                await getattr(self, on_event)(*args, **kwargs)
            if event in self._events:
                for callback in self._events[event]:
                    asyncio.create_task(callback(*args, **kwargs))
        except Exception as e:
            raise RuntimeError("Failure to emit")

    def cmd(self, description="", aliases=[]):
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
                self.commands.add(cmd)
            return cmd

        return decorator

    def add_cmd(self, coro, description="", aliases=[]):
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
            self.commands.add(cmd)

    async def process_commands(self, msg):
        """
        What is called in order to actually get command input and run commands

        Args:
            msg (str): The message containing command
        """
        context = Context(self, msg, self.http)

        asyncio.create_task(context.invoke())

    async def load_extension(self, name: str):
        """
        Load various extensions/plugins/cogs if any.

        Args:
            name (str): Name of the extension to load

        Raises:
            ModuleNotFoundError: If you suck and don't know the name of what you want to load
        """
        try:
            name = importlib.util.resolve_name(name, None)
        except Exception as e:
            raise ModuleNotFoundError(f"{name} does not exist")

        spec = importlib.util.find_spec(name)

        lib = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            raise ModuleNotFoundError(f"Spec could not be loaded {e}")
        try:
            ext = getattr(lib, 'Ext')
        except Exception as e:
            raise ModuleNotFoundError(f"Extension does not exist {e}")


        self.extensions.add(Extension(name=ext.name, description=ext.description, ext=ext))
        self.add_ext(Extension(name=ext.name, description=ext.description, ext=ext))


    def add_ext(self, ext):
        ext = ext.ext(self)



    def get_channel(self, channel_id: str):
        """
        Function to help retrieve channel from bot cache

        Args:
            channel_id (str): The channel id to search for

        Returns:
            Channel: The Channel object
        """
        for channel in self.user.private_channels:
            if channel_id == channel.id:
                return channel
        for guild in self.user.guilds:
            for channel in guild.channels:
                if channel_id == channel.id:
                    return channel

    def get_guild(self, guild_id: str):
        """
        Function to help retrieve guild from bot cache

        Args:
            guild_id (str): The guild id to search for

        Returns:
            Guild: The Guild object
        """
        for guild in self.user.guilds:
            if guild.id == guild_id:
                return guild

    async def get_user(self, user_id: str):
        """
        Function to retrieve user data. Probably need to be friends with them to retrieve the details.

        Args:
            user_id (Str): ID of the other user.

        Returns:
            User: The User object
        """
        data = await self.http.request(method="get", endpoint=f"/users/{user_id}")
        return User(data, self, self.http)

    async def add_friend(self, user_id: str):
        """
        Function to add random user as a friend.

        Args:
            user_id (str): ID of the possible random user.

        Returns:
            No return value.
        """
        await self.http.request(method="put", endpoint=f"/users/@me/relationships/{user_id}",
                                headers={"origin": "https://discord.com",
                                         "referer": f"https://discord.com/channels/@me/{random.choice(self.user.private_channels).id}"},
                                json={})

    async def edit_profile(self, bio: str = None, accent: int = None):
        """ Edits user profile
        """
        fields = {}
        if bio != None:
            fields['bio'] = bio
        if accent != None:
            fields['accent'] = accent
        await self.http.request(method="patch", endpoint=f"/users/@me/profile", json=fields)

    async def change_pfp(self, avatar_url=None):
        """Disclaimer: This may phone lock your account :(

        Args:
            avatar_url (str): URL of image

        Raises:
            TypeError: URL not specified
        """
        if avatar_url != None:
            image = await self.http.encode_image(avatar_url)
            await self.http.request(method="patch", endpoint="/users/@me", headers={"origin": "https://discord.com",
                                                                                    "referer": "https://discord.com/channels/@me"},
                                    json={'avatar': image})
        else:
            raise TypeError("Avatar url not specified")

    async def create_dm(self, recipient_id: int):
        """
        Function to create new DM Channel with other user. Can be used with bots too.

        Args:
            recipient_id (snowflake): ID of recipient - Has to be user or bot ID

        Raises:
            TypeError: Recipient ID not specified

        Returns:
            DMChannel object
        """
        if recipient_id is not None:
            data = await self.http.request(method="post", endpoint="/users/@me/channels",
                                           json={"recipient_id": recipient_id})
            return DMChannel(data, bot=self, http=self.http)
        else:
            raise TypeError("Recipient ID not specified")

    async def change_hypesquad(self, house: str):
        if house.lower() == "bravery":
            await self.http.request(method="post", endpoint = "/hypesquad/online", json = {"house_id": 1})
        if house.lower() == "brilliance":
            await self.http.request(method="post", endpoint = "/hypesquad/online", json = {"house_id": 2})
        if house.lower() == "balance":
            await self.http.request(method="post", endpoint = "/hypesquad/online", json = {"house_id": 3})

    async def change_presence(self, status: str, afk: bool=False, activity: dict=Activity.Game("test", "testing")):
        await self.gateway.change_presence(status, afk, activity=activity)



