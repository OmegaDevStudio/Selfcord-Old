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
        """Used to retrieve basic token information

        Args:
            token (str): User token

        Returns:
            Client: A Client object
        """
        self.token = token
        data = await self.request("get", "/users/@me")
        self.client = Client(data)
        return data

    async def request(self, method: str, endpoint: str, *args, **kwargs) -> dict:
        """Used to send requests

        Args:
            method (str): HTTP method
            endpoint (str): Discord api endpoint

        Raises:
            LoginFailure: If you suck

        Returns:
            dict: Data, json data
        """
        url = self.base_url + endpoint

        headers = {
            "cookie": "__dcfduid=1843e900f57311ebabfcfbf470034971; __sdcfduid=1843e901f57311ebabfcfbf47003497135c90a1bff5944460aef496a60343617f36974e907b33ca08e8d818ec2aa1a5e; _ga=GA1.2.1238853473.1633623071; __stripe_mid=a5ea391c-4c81-4c41-9b97-420d213223b54d9493; locale=en-GB; __cfruid=3b09207efeb15728a634740aeeed336cbf738872-1665786266",
            "authorization": self.token,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            'Content-Type': 'application/json',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJmciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM2MjQwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'X-Discord-Locale': 'en-US',
            'X-Debug-Options': 'bugReporterEnabled',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }
        async with ClientSession(headers=headers) as session:
            request = getattr(session, method)
            while True:
                async with request(url, *args, **kwargs) as resp:
                    if resp.status == 429:
                        try:
                            json = await resp.json()
                            await aprint(f"Ratelimited... Waiting before the request {json['retry_after']} seconds...")
                            await asyncio.sleep(json["retry_after"])
                            continue
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
                        await aprint(json)
                    elif resp.status == 201:
                        data = await resp.json()
                        break
                    elif resp.status == 204:
                        data = await resp.text()
                        break
                    elif resp.status == 200:
                        data = await resp.json()
                        break
                    else:
                        json = await resp.json()
                        raise LoginFailure(json, resp.status)
        return data

