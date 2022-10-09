import asyncio
from selfcord.api import gateway, http
from selfcord.models import Client
from selfcord.utils import Emitter

class Bot(Emitter):
    def __init__(self, show_beat: bool=False) -> None:
        self.show_beat = show_beat
        self.token = None
        self.http = http()
        self.gateway = gateway(show_beat)
        self.user = None



    def run(self, token: str):
        self.token = token
        async def runner():
            data = await self.http.static_login(token)
            self.user = Client(data)
            await self.gateway.start(token, self.user)
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass
