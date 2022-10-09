

from textwrap import wrap
from ..models import User
import asyncio
from aioconsole import aprint
import inspect

class EventHandler:
    def __init__(self):
        self._events = {}



    async def handle_ready(self, data, user):
        self.user = user
        





