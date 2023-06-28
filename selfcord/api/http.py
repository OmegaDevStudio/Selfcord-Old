from __future__ import annotations

import asyncio
import random
from base64 import b64encode
from traceback import format_exception
from typing import TYPE_CHECKING

import aiohttp
import ujson
from aioconsole import aprint
from aiohttp import ClientSession

from ..models import Client, User
from ..utils import logging

lib, _, _ = __name__.partition(".")
log = logging.getLogger(__name__)


class http:
    """Base HTTP class to aid making requests via discord api"""

    def __init__(self, debug=False) -> None:
        self.debug = debug
        xproperties = [
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJmciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTU0MTg2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkRpc2NvcmQgQ2xpZW50IiwicmVsZWFzZV9jaGFubmVsIjoiY2FuYXJ5IiwiY2xpZW50X3ZlcnNpb24iOiIwLjAuMTQwIiwib3NfdmVyc2lvbiI6IjUuMTkuMC0zLXJ0MTAtTUFOSkFSTyIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tR0IiLCJ3aW5kb3dfbWFuYWdlciI6IktERSx1bmtub3duIiwiZGlzdHJvIjoiXCJNYW5qYXJvIExpbnV4XCIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxNTQyMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9",
            "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA2LjAuMC4wIiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiaHR0cHM6Ly93d3cucm9ibG94LmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluIjoid3d3LnJvYmxveC5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTU0MTg2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        ]
        self.cookies = {}
        self.token = None
        self.xproperties = random.choice(xproperties)
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
        if self.debug:
            log.debug("Finished Static login")
            log.info(f"Gathered information on {self.client}")
        return data

    async def get_cookie(self):
        """Gather cookie for user upon client start"""
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.get(
                "https://discord.com",
                headers={
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"
                },
            ) as resp:
                dcf = resp.headers["set-cookie"].split("__dcfduid=")[0].split(";")[0]
                sdc = resp.headers["set-cookie"].split("__sdcfduid=")[0].split(";")[0]
                cfr = resp.headers["set-cookie"].split("__cfruid=")[0].split(";")[0]

                self.cookies["dcf"] = self.cookies.get("dcf") if dcf != "" else ""
                self.cookies["sdc"] = self.cookies.get("sdc") if sdc != "" else ""
                self.cookies["cfr"] = self.cookies.get("cfr") if cfr != "" else ""
                self.cookie = set(self.cookies)

            async with session.get(
                "https://discord.com/api/v9/experiments",
                headers={
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.139 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"
                },
            ) as resp:
                json = await resp.json()
                self.fingerprint = json["fingerprint"]
        if self.debug:
            log.debug("Gathered cookie and fingerprint")
            log.info(f"Fingerprint Gathered: {self.fingerprint}")

    def remove_dupes(self, dictionary: dict):
        return set(dictionary)

    async def request(self, method: str, endpoint: str, *args, **kwargs) -> dict | None:
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
            "Content-Type": "application/json",
            "X-Super-Properties": self.xproperties,
            "X-Discord-Locale": "en-GB",
            "X-context-properties": "eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6bnVsbCwibG9jYXRpb25fY2hhbm5lbF9pZCI6IjEwOTkwOTMxODEyNTUxNDM1MjUiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjEsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiIxMTE2NTE0MDMyODk2MTgwMjU0In0=",
            "connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "origin": "https://discord.com",
            "DNT": "1",
            "x-debug-options": "logGatewayEvents,logOverlayEvents,logAnalyticsEvents,bugReporterEnabled",
            "x-fingerprint": self.fingerprint,
            "x-discord-timezone": "Europe/London",
            "TE": "trailers",
        }

        async with ClientSession(
            json_serialize=ujson.dumps,
            timeout=aiohttp.ClientTimeout(
                total=10000, connect=10000, sock_read=10000, sock_connect=10000
            ),
            connector=aiohttp.TCPConnector(
                limit=0, limit_per_host=0, ttl_dns_cache=300
            ),
            headers=headers,
        ) as session:
            request = getattr(session, method)
            while True:
                async with request(url, *args, **kwargs) as resp:
                    if self.debug:
                        log.debug(f"Sent Request Method: {method} URL: {url} Payload: {args} {kwargs}")

                    if resp.status == 429:
                        try:
                            json = await resp.json()
                            await asyncio.sleep(json["retry_after"])
                            log.error(f"429 Ratelimited: {json}")
                            continue
                        except Exception as e:
                            error = "".join(format_exception(e, e, e.__traceback__))
                            text = await resp.text()
                            
                            log.error(f"Error upon parsing json : {text}")
                            log.error(f"Error upon parsing json : \n{error}")
                            log.info(
                                f"Attempted to send request to URL: {url} PAYLOAD: {kwargs}"
                            )
                            await aprint(error)
                            return None

                    elif resp.status == 401:
                        json = await resp.json()
                        log.error(f"{json} -- {resp.status}")
                        await aprint(json)
                        return None

                    elif resp.status == 403:
                        json = await resp.json()
                        log.error(f"403 Unauthorized: {json}")
                        log.info(
                            f"Attempted to send request to URL: {url} PAYLOAD: {args} {kwargs}"
                        )
                        await aprint(json)
                        return None

                    elif resp.status == 201:
                        data = await resp.json()
                        break

                    elif resp.status == 204:
                        data = await resp.text()
                        break

                    elif resp.ok:
                        data = await resp.json()
                        break

                    else:
                        if self.debug:
                            log.error(f"Unknown Error: {resp.status}")
                            log.info(
                                f"Attempted to send request to URL: {url} PAYLOAD: {args} {kwargs}"
                            )
                        try:
                            json = await resp.json()
                            await aprint(json)
                            return None
                        except Exception as e:
                            error = "".join(format_exception(e, e, e.__traceback__))
                            log.error(f"Unable to log response: \n{error}")
                            await aprint(error)
                            return None
        try:
            if resp.headers["set-cookie"]:
                dcf = resp.headers["set-cookie"].split("__dcfduid=")[0].split(";")[0]
                sdc = resp.headers["set-cookie"].split("__sdcfduid=")[0].split(";")[0]
                cfr = resp.headers["set-cookie"].split("__cfruid=")[0].split(";")[0]
                bm = resp.headers["set-cookie"].split("__cf_bm=")[0].split(";")[0]

                self.cookies["dcf"] = self.cookies.get("dcf") if dcf != "" else ""
                self.cookies["sdc"] = self.cookies.get("sdc") if sdc != "" else ""
                self.cookies["cfr"] = self.cookies.get("cfr") if cfr != "" else ""
                self.cookies["bm"] = self.cookies.get("bm") if bm != "" else ""
                self.cookie = set(self.cookies)
        except:
            pass

        try:
            return data
        except:
            return None

    async def encode_image(self, url: str) -> str:
        """Turn an image url into a b64 payload

        Args:
            url (str): The URL of the image

        Returns:
            str: The b64 payload
        """
        async with ClientSession() as session:
            async with session.get(f"{url}") as resp:
                image = b64encode(await resp.read())
                newobj = str(image).split("'", 2)
        if self.debug:
            log.debug("Finished encoding image")
            log.info(f"Encoded Image: {url}")
        return f"data:image/png;base64,{newobj[1]}"
