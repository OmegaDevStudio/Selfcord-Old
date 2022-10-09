import asyncio
from selfcord.api import gateway, http
import inspect
from selfcord.models import Client
from collections import defaultdict
from aioconsole import aprint


class Bot():
    def __init__(self, show_beat: bool=False) -> None:
        self.show_beat = show_beat
        self.token = None
        self.http = http()
        self.gateway = gateway(show_beat)
        self.user = None
        self._events = defaultdict(list)

    def run(self, token: str):
        self.token = token
        async def runner():
            data = await self.http.static_login(token)
            self.user = Client(data)
            await self.gateway.start(token, self.user, self)
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    def on(self, event: str):
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
        on_event = "on_{}".format(event)
        try:
            if hasattr(self, on_event):
                await getattr(self, on_event)(*args, **kwargs)
            if event in self._events:
                for callback in self._events[event]:
                    asyncio.create_task(callback(*args, **kwargs))
        except Exception as e:
            await aprint(e)

