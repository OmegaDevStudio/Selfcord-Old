from aiohttp import ClientSession
from aioconsole import aprint
import asyncio
from base64 import b64encode

import aiohttp
from selfcord.api.errors import LoginFailure


from ..models import User, Client

class http:
    def __init__(self) -> None:
        self.token = None
        self.cookies = {}
        self.base_url = "https://discord.com/api/v9"


    async def static_login(self, token: str):
        """Used to retrieve basic token information

        Args:
            token (str): User token

        Returns:
            Client: A Client object
        """
        await self.get_cookie()
        self.token = token
        data = await self.request("get", "/users/@me")
        self.client = Client(data)
        return data

    async def get_cookie(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com", headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"}) as resp:
                dcf = resp.headers['set-cookie'].split("__dcfduid=")[0].split(";")[0]
                sdc = resp.headers['set-cookie'].split("__sdcfduid=")[0].split(";")[0]
                cfr = resp.headers['set-cookie'].split("__cfruid=")[0].split(";")[0]
                if dcf != "":
                    self.cookies['dcf'] = dcf
                else:
                    self.cookies['dcf'] = ""
                if sdc != "":
                    self.cookies['sdc'] = sdc
                else:
                    self.cookies['sdc'] = ""
                if cfr != "":
                    self.cookies['cfr'] = cfr
                else:
                    self.cookies['cfr'] = ""
                self.cookie = ""
                for value in self.remove_dupes(self.cookies).values():
                    if value != "":
                        self.cookie += f"{value}; "

    def remove_dupes(self, item: dict):
        result = {}
        for key, value in item.items():
            if value not in result.values():
                result[key] = value
        return result



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
            "cookie": f"{self.cookie}",
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
        if resp.headers['set-cookie'] != None:
            dcf = resp.headers['set-cookie'].split("__dcfduid=")[0].split(";")[0]
            sdc = resp.headers['set-cookie'].split("__sdcfduid=")[0].split(";")[0]
            cfr = resp.headers['set-cookie'].split("__cfruid=")[0].split(";")[0]
            bm = resp.headers['set-cookie'].split("__cf_bm=")[0].split(";")[0]
            if dcf != "":
                self.cookies['dcf'] = dcf
            if sdc != "":
                self.cookies['sdc'] = sdc
            if cfr != "":
                self.cookies['cfr'] = cfr
            if bm != "":
                self.cookies['bm'] = bm
            self.cookie = ""
            for value in self.remove_dupes(self.cookies).values():
                if value != "":
                    self.cookie += f"{value}; "

        
        return data

    async def encode_image(self, url):
        async with ClientSession() as session:
            async with session.get(f"{url}") as resp:
                image = b64encode(await resp.read())
                newobj = str(image).split("'", 2)
        return f"data:image/png;base64,{newobj[1]}"

