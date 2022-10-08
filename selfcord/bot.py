import asyncio
from selfcord.api import gateway
from selfcord.api import http

class Bot:
    def __init__(self) -> None:
        self.token = None
        self.http = http()

    async def run(self, token: str):
        self.token = token
        await self.http.static_login(token)
