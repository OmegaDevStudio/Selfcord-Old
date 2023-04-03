import asyncio
import json
import time
import zlib
from traceback import format_exception
from typing import Dict, Any, Union, Optional, List, Generator

import aiohttp
import websockets
from aioconsole import aprint

from selfcord.models.client import Client
from .errors import ReconnectWebsocket
from .events import EventHandler
from .http import Http


class Activity:
    @staticmethod
    async def create_payload(
        name: str, details: str, state: str, buttons: Dict[Any, Any],
        application_id: Union[str, int], key: str, type_: int, url: str = None
    ) -> Optional[Dict[Any, Any]]:
        button_urls = [button for button in buttons.values()]
        buttons = [button for button in buttons.keys()]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://discordapp.com/api/oauth2/applications/{application_id}/assets") as response:
                if response.status == 200:
                    for item in await response.json():
                        if item.get('name') == key:
                            key = item['id']
                            break

        payload = {
            "name": name,
            "details": details,
            "state": state,
            "application_id": application_id,
            "assets": {"large_image": key},
            "type": type_,
            "created_at": int(time.time()),
        }

        if url:
            payload['url'] = url

        if buttons and button_urls:
            payload['buttons'] = buttons
            payload['metadata'] = {'button_urls': button_urls}

        return payload

    @staticmethod
    async def game(
        name: str, details: str = "", state: str = "", buttons: Optional[Dict[Any, Any]] = None,
        application_id: str = "1072088555528138782", key: str = "dolphine"
    ) -> Optional[Dict[Any, Any]]:
        if buttons is None:
            buttons = {}

        type_ = 0
        return await Activity.create_payload(name, details, state, buttons, application_id, key, type_)

    @staticmethod
    async def stream(
        name: str, details: str = "", state: str = "",
        url: str = "https://www.youtube.com/watch?v=CyIrJVp-sH8", buttons: Optional[Dict[Any, Any]] = None,
        application_id: str = "1037788701318729799", key: str = "dolphine"
    ) -> Optional[Dict[Any, Any]]:
        if buttons is None:
            buttons = {}

        type_ = 1
        return await Activity.create_payload(name, details, state, buttons, application_id, key, type_, url)

    @staticmethod
    async def listen(
        name: str, details: str = "", state: str = "", buttons: Optional[Dict[Any, Any]] = None,
        application_id: str = "1037788701318729799", key: str = "dolphine"
    ) -> Optional[Dict[Any, Any]]:
        if buttons is None:
            buttons = {}

        type_ = 2
        return await Activity.create_payload(name, details, state, buttons, application_id, key, type_)

    @staticmethod
    async def watch(
        name: str, details: str = "", state: str = "", buttons: Optional[Dict[Any, Any]] = None,
        application_id: str = "1037788701318729799", key: str = "dolphine"
    ) -> Optional[Dict[Any, Any]]:
        if buttons is None:
            buttons = {}

        type_ = 3
        return await Activity.create_payload(name, details, state, buttons, application_id, key, type_)


class Gateway:
    # OP CODES
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

    def __init__(self, http: Http, show_heartbeat=False):
        self.token = None
        self.user = None
        self.bot = None
        self.handler = None
        self.ws = None
        self.show_heartbeat = show_heartbeat
        self.http: Http = http
        self.zlib = zlib.decompressobj()
        self.zlib_suffix = b'\x00\x00\xff\xff'
        self.last_ack = time.perf_counter()
        self.last_send = time.perf_counter()
        self.latency = float('inf')
        self.alive = False

    async def recv_msg(self) -> None:
        """
        Receives Message from gateway, encodes as json and does things depending on op code
        """

        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix:
            return

        if item:
            item = self.zlib.decompress(item)
            item = json.loads(item)  # Get json message from gateway

            op = item.get('op')  # Op code
            data = item.get('d')  # Data
            event = item.get('t')  # The event

            if op == self.RECONNECT:
                await self.close()
                raise ReconnectWebsocket('Connection was closed.')

            elif op == self.INVALIDATE_SESSION:
                if data:
                    await self.close()
                    raise ReconnectWebsocket('Connection was closed.')

            elif op == self.HELLO:
                # Begins heartbeat and sends identify if this op is received
                interval = data['heartbeat_interval'] / 1000.0
                await self.identify()
                asyncio.create_task(self.heartbeat(interval))

            elif op == self.HEARTBEAT_ACK:
                await self.heartbeat_ack()

            elif op == self.DISPATCH:
                # If op is 0 it signifies a regular gateway event
                # These events are discord events like message_create, role_create whatever.

                handle = f'handle_{event.lower()}'

                if hasattr(self.handler, handle):  # If the event handler exists, so e.g handle_ready
                    method = getattr(self.handler, handle)

                    val = await asyncio.gather(
                        asyncio.create_task(method(data, self.user, self.http)),
                        return_exceptions=True
                    )  # A background task is created to run the handler
                    for item in val:
                        if item is not None:
                            await self.bot.emit("error", item)
                        break

                    # asyncio.create_task(method(data, self.user, self.http))
                # Handlers are all situated in events.py

    @staticmethod
    def roundup(n) -> int:
        import math
        return int(math.ceil(n / 100.0)) * 100

    @staticmethod
    def chunks(lst: List[Any], n: int) -> Generator[List[Any], None, None]:
        for i in range(0, len(lst), 1):
            if len(lst[:i + 1]) > 3:
                for i in range(i, len(lst), n):
                    yield lst[i:i + n]
                break

            yield lst[:i + 1]

    async def change_presence(
        self, status: str, afk: bool = False,
        activity=None
    ) -> None:
        """Change the clients current presence

        Args:
            status (str): online, offline or dnd
            afk (bool): Whether client is set as AFK
            activity (Activity): Activity object
        """
        if activity is None:
            activity = await Activity.game("Selfcord", "Greatest wrapper")

        payload = {
            "op": self.PRESENCE,
            "d": {
                "since": time.time(),
                "activities": [activity],
                "status": status.lower(),
                "afk": afk
            },
        }

        await self.send_json(payload)

    async def lazy_chunk(self, guild_id: str, channel_id: str, amount: int) -> None:
        """Sends lazy guild request to gather current online members

        Args:
            guild_id (str): The guild id specified
            channel_id (str): The channel id specified
            amount (int): The amount of members
        """

        ranges = []

        for i in range(0, amount, 100):
            ranges.append([i, self.roundup(i + (amount - i)) - 1]) if i + 99 > amount else ranges.append([i, i + 99])

        for item in self.chunks(ranges, 3):
            payload = {
                'op': 14,
                'd': {
                    'guild_id': guild_id,
                    'typing': True,
                    'channels': {channel_id: item}
                }
            }

            await self.send_json(payload)

    async def send_json(self, payload: Dict[Any, Any]) -> None:
        """Send json to the gateway

        Args:
            payload (dict): Valid payload to send to the gateway
        """
        await self.ws.send(json.dumps(payload))

    async def connect(self) -> None:
        """Connect to discord gateway"""
        self.ws = await websockets.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream',
                                           origin='https://discord.com')
        self.alive = True

    async def close(self) -> None:
        """Close the connection to discord gateway"""
        self.alive = False
        await self.ws.close()

    async def identify(self) -> None:
        """Identify to gateway, uses amazing mobile client spoof"""
        payload = {
            'op': 2,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': 'android',
                    '$browser': 'Discord Android',
                    '$device': 'Discord Android',
                    '$referrer': '',
                    '$referring_domain': ''
                },
            }
        }
        await self.send_json(payload)

    async def heartbeat(self, interval: Union[int, float]) -> None:
        """Heartbeat for gateway to maintain connection

        Args:
            interval (int): Interval between sends
        """
        await aprint(f'Heartbeat loop has began with the interval of {interval} seconds!')
        heartbeat_json = {
            'op': self.HEARTBEAT,
            'd': time.time()
        }
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeat_json)
            self.last_send = time.perf_counter()
            if self.show_heartbeat:
                await aprint('Sent Beat')

    async def heartbeat_ack(self) -> None:
        """Whenever heartbeat ack is sent, logs the time between last send of heartbeat json and receive of the ack"""
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send

    async def start(self, token: str, user: Client, bot: Any) -> None:
        """Start discord gateway connection

        Args:
            token (str): User token
            user (Client): User client
            bot (_type_): Bot class
        """
        self.handler = EventHandler(bot, self.http)
        self.bot = bot

        await self.bot.inbuilt_commands()  # In built commands very cool

        self.user = user
        self.token = token

        await self.connect()
        while self.alive:
            try:
                await self.recv_msg()
            except KeyboardInterrupt:
                await aprint('Shutting down...')
                await self.close()
            except Exception as e:
                error = "".join(format_exception(type(e), e, e.__traceback__))
                await self.bot.emit("error", error)
                await self.close()

    async def ring(self, channel: Union[str, int], guild: Union[str, int] = None) -> None:
        payload = {
            "op": self.VOICE_STATE,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "preferred_region": "rotterdam",
                "self_mute": False,
                "self_deaf": False,
                "self_video": True,
            }
        }
        await self.send_json(payload)
        await self.http.request(method="post", endpoint=f"/channels/{channel}/call/ring", json={"recipients": None})

    async def leave_call(self) -> None:
        payload = {
            "op": self.VOICE_STATE,
            "d": {
                "guild_id": None,
                "channel_id": None,
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            }
        }
        await self.send_json(payload)
