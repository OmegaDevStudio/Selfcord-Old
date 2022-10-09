from aiohttp import ClientSession
from aioconsole import aprint
import asyncio

from selfcord.api.errors import LoginFailure


from ..models import User, Client

class http:
    def __init__(self) -> None:
        self.token = None
        self.base_url = "https://discord.com/api/v9"


    async def static_login(self, token: str):
        self.token = token
        data = await self.request("get", "/users/@me")
        self.client = Client(data)
        return data

    async def request(self, method: str, endpoint: str, *args, **kwargs) -> dict:
        url = self.base_url + endpoint

        headers = {
            "authorization": self.token,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "content-type": "application/json"
        }
        while True:
            async with ClientSession(headers=headers) as session:
                request = getattr(session, method)
                async with request(url, *args, **kwargs) as resp:
                    if resp.status == 429:
                        try:
                            json = await resp.json()
                            await asyncio.sleep(json["retry_after"])
                            await aprint(f"Ratelimited... Waiting before the request {json['retry_after']} seconds...")
                        except Exception as e:
                            await aprint(f"Error: {e}")
                            text = await resp.text()
                            await aprint(text)
                            break
                    elif resp.status == 401:
                        json = await resp.json()
                        raise LoginFailure(json, resp.status)
                    elif resp.status == 403:
                        json = await resp.json()
                        raise LoginFailure(json, resp.status)
                    elif resp.status == 201:
                        data = await resp.json()
                        break
                    elif resp.status == 204:
                        data = await resp.json()
                        break
                    elif resp.status == 200:
                        data = await resp.json()
                        break
                    else:
                        json = await resp.json()
                        raise LoginFailure(json, resp.status)


        return data

