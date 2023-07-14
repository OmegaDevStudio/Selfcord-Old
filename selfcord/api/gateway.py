from __future__ import annotations

import asyncio
import os
import time
import zlib
from traceback import format_exception

import requests
import ujson
import websockets

from selfcord.models.client import Client

from ..utils import logging
from .errors import ReconnectWebsocket
from .events import EventHandler

log = logging.getLogger(__name__)


class Activity:
    @staticmethod
    def Game(
        name: str,
        details: str,
        state: str,
        buttons: dict,
        application_id: str,
        key: str,
    ) -> dict[str, int]:
        """Method to generate activity dict for the "Playing ..." payload

        Args:
            name (str): Name of the activity
            details (str): Details of the activity
            state (str): State of the activity
            buttons (dict): Buttons for the activity.
            Example:
                { "My Website": "https://google.com"}
            application_id (str): Application ID
            key (str): Key for the large image

        Returns:
            dict[str, int]: Dict for the activity object for payload
        """
        type = 0
        button_urls = list(buttons.values())
        buttons: list = list(buttons.keys())
        req = requests.get(
            f"https://discordapp.com/api/oauth2/applications/{application_id}/assets"
        )
        for item in req.json():
            if item["name"] == key:
                key = item["id"]

        return (
            {
                "name": name,
                "details": details,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "type": type,
                "created_at": int(time.time()),
            }
            if not button_urls or not buttons
            else {
                "name": name,
                "details": details,
                "type": type,
                "buttons": buttons,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "metadata": {
                    "button_urls": button_urls,
                },
                "created_at": int(time.time()),
            }
        )

    @staticmethod
    def Stream(
        name: str,
        details: str,
        state: str,
        url: str,
        buttons: dict,
        application_id: str,
        key: str,
    ) -> dict[str, int]:
        """Method to generate activity dict for the "Streaming ..." payload

        Args:
            name (str): Name of the activity
            details (str): Details of the activity
            state (str): State of the activitiy
            url (str): URL for streaming
            buttons (dict): Buttons for the activity.
            Example:
                { "My Website": "https://google.com"}
            application_id (str): Application ID
            key (str): Key for the large image

        Returns:
            dict[str, int]: Dict for the activity object for payload
        """
        type = 1
        button_urls = list(buttons.values())
        buttons: list = list(buttons.keys())
        req = requests.get(
            f"https://discordapp.com/api/oauth2/applications/{application_id}/assets"
        )
        for item in req.json():
            if item["name"] == key:
                key = item["id"]

        return (
            {
                "name": name,
                "details": details,
                "type": type,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "created_at": int(time.time()),
                "url": url,
            }
            if not button_urls or not buttons
            else {
                "name": name,
                "details": details,
                "type": type,
                "buttons": buttons,
                "url": url,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "metadata": {
                    "button_urls": button_urls,
                },
                "created_at": int(time.time()),
            }
        )

    @staticmethod
    def Listen(
        name: str,
        details: str,
        state: str,
        buttons: dict,
        application_id: str,
        key: str,
    ) -> dict[str, int]:
        """Method to generate activity dict for the "Listening ..." payload

        Args:
            name (str): Name of the activity
            details (str): Details of the activity
            state (str): State of the activity
            buttons (dict): Buttons for the activity.
            Example:
                { "My Website": "https://google.com"}
            application_id (str): Application ID
            key (str): Key for the large image

        Returns:
            dict[str, int]: Dict for the activity object for payload
        """
        type = 2
        button_urls = list(buttons.values())
        buttons: list = list(buttons.keys())
        req = requests.get(
            f"https://discordapp.com/api/oauth2/applications/{application_id}/assets"
        )
        for item in req.json():
            if item["name"] == key:
                key = item["id"]

        return (
            {
                "name": name,
                "details": details,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "type": type,
                "created_at": int(time.time()),
            }
            if not button_urls or not buttons
            else {
                "name": name,
                "details": details,
                "type": type,
                "buttons": buttons,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "metadata": {
                    "button_urls": button_urls,
                },
                "created_at": int(time.time()),
            }
        )

    @staticmethod
    def Watch(
        name: str,
        details: str,
        state: str,
        buttons: dict,
        application_id: str,
        key: str,
    ) -> dict[str, int]:
        """Method to generate activity dict for the "Watching ..." payload

        Args:
            name (str): Name of the activity
            details (str): Details of the activity
            state (str): State of the activity
            buttons (dict): Buttons for the activity.
            Example:
                { "My Website": "https://google.com"}
            application_id (str): Application ID
            key (str): Key for the large image

        Returns:
            dict[str, int]: Dict for the activity object for payload
        """
        type = 3

        button_urls = list(buttons.values())
        buttons: list = list(buttons.keys())

        req = requests.get(
            f"https://discordapp.com/api/oauth2/applications/{application_id}/assets"
        )
        for item in req.json():
            if item["name"] == key:
                key = item["id"]

        return (
            {
                "name": name,
                "details": details,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "type": type,
                "created_at": int(time.time()),
            }
            if not button_urls or not buttons
            else {
                "name": name,
                "details": details,
                "type": type,
                "buttons": buttons,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "metadata": {
                    "button_urls": button_urls,
                },
                "created_at": int(time.time()),
            }
        )


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zlib import _Decompress

    from .http import http


class gateway:
    """Discord Gateway instance, used to initialise gateway connections"""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __init__(self, http: http, debug: bool = False):
        self.debug: bool = debug
        self.http: http = http
        self.zlib: _Decompress = zlib.decompressobj()
        self.zlib_suffix: bytes = b"\x00\x00\xff\xff"
        self.last_ack: float = time.perf_counter()
        self.last_send: float = time.perf_counter()
        self.latency = float("inf")
        self.resume_url = None
        self.alive = False
        self.fired = False

    async def recv_msg(self):
        """
        Receives Message from gateway, encodes as json and does things depending on op code
        """
        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix:
            return

        if item:
            if self.fired:
                log.info(f"{item}")
            try:
                item = self.zlib.decompress(item)
            except Exception as e:
                log.error(f"Could not decompress\n{e}")
                return
            item = ujson.loads(item)  # Get json message from gateway

            op = item.get("op")  # Op code
            data = item.get("d")  # Data
            event = item.get("t")  # The event
            if op == self.RECONNECT:
                await self.close()
                log.info(f"DATA: {data}\nOP: {op}\nEVENT: {event}")
                await asyncio.sleep(10)
                await self.connect()
                self.fired = True
                log.error("Reconnect websocket")

            elif op == self.INVALIDATE_SESSION:
                if data:
                    await self.close()
                    log.error("Session Invalidated")

            elif op == self.HELLO:
                # Begins heartbeat and sends identify if this op is received
                interval = data["heartbeat_interval"] / 1000.0
                await self.identify()
                asyncio.create_task(self.heartbeat(interval))

            elif op == self.HEARTBEAT_ACK:
                await self.heartbeat_ack()

            elif op == self.DISPATCH:
                # If op is 0 it signifies a regular gateway event
                # These events are discord events like message_create, role_create whatever.

                handle = f"handle_{event.lower()}"

                if hasattr(
                    self.handler, handle
                ):  # If the event handler exists, so e.g handle_ready
                    method = getattr(self.handler, handle)

                    val = await asyncio.gather(
                        asyncio.create_task(method(data, self.user, self.http)),
                        return_exceptions=True,
                    )  # A background task is created to run the handler
                    for item in val:
                        if item is None:
                            break
                        error = "".join(format_exception(item, item, item.__traceback__))
                        log.error(f"Error occurred when handling events\n {error}")
                        await self.bot.emit("error", item)

                    # asyncio.create_task(method(data, self.user, self.http))
                # Handlers are all situated in events.py

    def roundup(self, n):
        import math

        return int(math.ceil(n / 100.0)) * 100

    def chunks(self, lst, n):
        for i in range(0, len(lst), 1):
            if len(lst[: i + 1]) > 3:
                for i in range(i, len(lst), n):
                    yield lst[i : i + n]
                break

            yield lst[: i + 1]

    async def change_presence(self, status: str, afk: bool, activity: dict):
        """Change the clients current presence

        Args:
            status (str): online, offline or dnd
            afk (bool): Whether client is set as AFK
            activity (Activity): Activity object
        """
        payload = {
            "op": 3,
            "d": {
                "since": time.time(),
                "activities": [activity],
                "status": status.lower(),
                "afk": afk,
            },
        }

        await self.send_json(payload)
        if self.debug:
            log.debug("Began rich presence")
            log.info(f"{activity}")

    async def lazy_chunk(self, guild_id: str, channel_id: str, amount: int):
        """Sends lazy guild request to gather current online members

        Args:
            guild_id (str): The guild id specified
            channel_id (str): The channel id specified
        """

        ranges = []

        for i in range(0, amount, 100):
            ranges.append(
                [i, self.roundup(i + (amount - i)) - 1]
            ) if i + 99 > amount else ranges.append([i, i + 99])

        for item in self.chunks(ranges, 3):
            payload = {
                "op": 14,
                "d": {
                    "guild_id": guild_id,
                    "typing": True,
                    "channels": {channel_id: item},
                },
            }

            await self.send_json(payload)
            await asyncio.sleep(2.0)

        if self.debug:
            log.debug("Finished guild lazy chunking")
            log.info(f"Subscription to GUILD: {guild_id} with CHANNEL: {channel_id}")

    async def send_json(self, payload: dict):
        """Send json to the gateway

        Args:
            payload (dict): Valid payload to send to the gateway
        """
        await self.ws.send(ujson.dumps(payload))

    async def reconnect(self, seq: int):
        """Reconnect to discord gateway"""
        self.ws = await websockets.connect(
            f"{self.bot.resume_url}?encoding=json&v=9&compress=zlib-stream"
        )
        self.alive = True
        await asyncio.sleep(1.5)
        payload = {
            "op": 6,
            "d": {"token": self.token, "session_id": self.bot.session_id, "seq": seq},
        }
        await self.send_json(payload)


    async def connect(self):
        """Connect to discord gateway"""
        self.ws = await websockets.connect(
            "wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream",
            origin="https://discord.com",
            max_size=None,
        )
        self.alive = True
        if self.debug:
            log.debug("Established connection to Discord Gateway")

    async def close(self):
        """Close the connection to discord gateway"""
        self.alive = False
        await self.ws.close()
        if self.debug:
            log.debug("Closed connection to discord gateway")

    async def identify(self):
        """Identify to gateway, uses amazing mobile client spoof"""
        
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "client_state": {
                    "api_code_version": 0,
                    "highest_last_message_id": "0",
                    "initial_guild_id": None,
                    "private_channels_version": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                },
                "compress": False,
                "presence": {
                    "activities": [],
                    "afk": False,
                    "since": 0,
                    "status": "dnd"
                },
                "properties": {
                    "os": "Android",
                    "browser": "Discord Android",
                    "device": "Discord Android",
                    "browser_useragent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.157 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
                    "system-locale": "en-GB",
                    "os_arch": "x64"
                },
            },
        }
        await self.send_json(payload)
        if self.debug:
            log.debug("Sent identify payload")
            log.info(f"Idenitified with {self.token} under Discord Android")

    async def heartbeat(self, interval):
        """Heartbeat for gateway to maintain connection

        Args:
            interval (int): Interval between sends
        """
        log.info(f"Heartbeat loop has begun with the interval of {interval} seconds!")
        heartbeatJSON = {"op": 1, "d": time.time()}
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            self.last_send = time.perf_counter()
            if self.debug:
                log.debug("Sent heartbeat")
                log.info(f"Delay since last heartbeat {self.latency:0.2f}ms")

    async def heartbeat_ack(self):
        """Whenever heartbeat ack is sent, logs the time between last send of heartbeat json and receive of the ack"""
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send

    async def start(self, token: str, user: Client, bot):
        """Start discord gateway connection

        Args:
            token (str): User token
            user (Client): User client
            bot (_type_): Bot class
        """
        self.handler = EventHandler(bot, self.http, self.debug)
        self.bot = bot

        await self.bot.inbuilt_commands()  # In built commands very cool

        self.user = user
        self.token = token

        await self.connect()
        while self.alive:
            try:
                await self.recv_msg()
            except KeyboardInterrupt:
                log.critical("Shutting down...")
                await self.close()
            except Exception as e:
                error = "".join(format_exception(e, e, e.__traceback__))
                await self.bot.emit("error", error)
                if self.debug:
                    log.error(f"Websocket Unexpectedly closed\n{error}")
                await self.close()

    async def video_call(self, channel: str, guild=None):
        """Initiates a discord video call

        Args:
            channel (str): Channel ID
            guild (str, optional): Guild ID. Defaults to None.
        """
        payload = {
            "op": 4,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "preferred_region": "rotterdam",
                "self_mute": False,
                "self_deaf": False,
                "self_video": True,
            },
        }
        await self.send_json(payload)
        if self.debug:
            log.debug("Initiated video call")
            log.info(f"Began video call to GUILD: {guild} and CHANNEL: {channel}")
        if guild is None:
            await self.http.request(
                method="post",
                endpoint=f"/channels/{channel}/call/ring",
                json={"recipients": None},
            )
            if self.debug:
                log.debug("Sent Ring")

    async def call(self, channel: str, guild=None):
        """Initiates a discord call

        Args:
            channel (str): Channel ID
            guild (str, optional): Guild ID. Defaults to None.
        """
        payload = {
            "op": 4,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "preferred_region": "rotterdam",
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            },
        }
        await self.send_json(payload)
        if self.debug:
            log.debug("Initiated call")
            log.info(f"Began call to GUILD: {guild} and CHANNEL: {channel}")
        if guild is None:
            await self.http.request(
                method="post",
                endpoint=f"/channels/{channel}/call/ring",
                json={"recipients": None},
            )
            if self.debug:
                log.debug("Sent Ring")

    async def stream_call(self, channel: str, guild=None):
        """Initiates a discord stream call

        Args:
            channel (str): Channel ID
            guild (str, optional): Guild ID. Defaults to None.
        """
        await self.call(channel, guild)
        type = "guild" if guild != None else "call"
        payload = {
            "op": 18,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "preferred_region": "rotterdam",
                "type": type,
            },
        }
        await self.send_json(payload)
        if self.debug:
            log.debug("Initiated call")
            log.info(f"Began call to GUILD: {guild} and CHANNEL: {channel}")
        if guild is None:
            await self.http.request(
                method="post",
                endpoint=f"/channels/{channel}/call/ring",
                json={"recipients": None},
            )

            payload = {
                "op": 22,
                "d": {"stream_key": f"call:{channel}:{self.user.id}", "paused": False},
            }
            if self.debug:
                log.debug("Initiated streaming")
                log.info(f"Began stream to CHANNEL: {channel}")
        else:
            payload = {
                "op": 22,
                "d": {
                    "stream_key": f"guild:{guild}:{channel}:{self.user.id}",
                    "paused": False,
                },
            }
            if self.debug:
                log.debug("Initiated streaming")
                log.info(f"Began stream to GUILD: {guild} and CHANNEL: {channel}")

        await self.send_json(payload)

    async def leave_call(self):
        """Leaves a discord call"""
        payload = {
            "op": 4,
            "d": {
                "guild_id": None,
                "channel_id": None,
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            },
        }
        await self.send_json(payload)
        if self.debug:
            log.debug("Left Voice call")
        if hasattr(self.bot, "voice"):
            await self.bot.voice.close()
            delattr(self.bot, "voice")
        if self.debug:
            log.info("Voice attribute for bot has been deleted")
