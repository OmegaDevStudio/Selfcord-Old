import inspect
from aioconsole import aprint
import asyncio

class Emitter:
    def __init__(self) -> None:
        self._events = {}


    def on(self, event, callback=None):
        if inspect.iscoroutinefunction(callback):
            self._events[event].append(callback)
        else:
            def wrapper(coro):
                if not inspect.iscoroutinefunction(coro):
                    raise RuntimeError("Not a coroutine!")
                self._events[event].append(coro)
                return coro
            return wrapper

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