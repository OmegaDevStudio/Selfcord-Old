import asyncio
from selfcord.api import gateway, http
from selfcord.utils import Emitter

class Bot(Emitter):
    def __init__(self, show_beat: bool) -> None:
        self.show_beat = show_beat
        self.token = None
        self.http = http()
        self.gateway = gateway(show_beat)

    def run(self, token: str):
        self.token = token
        async def runner():
            await self.http.static_login(token)
            await self.gateway.start(token)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass
