import asyncio
import websockets
from aioconsole import aprint
import json
import time
import zlib
from selfcord.api.events import EventHandler
from selfcord.api.errors import ReconnectWebsocket
from selfcord.models.client import Client



class gateway:
    def __init__(self, http, show_heartbeat=False):
        self.show_heartbeat = show_heartbeat
        self.http = http
        self.zlib = zlib.decompressobj()
        self.zlib_suffix = b"\x00\x00\xff\xff"
        self.last_ack = time.perf_counter()
        self.last_send = time.perf_counter()
        self.latency = float('inf')
        self.alive = False


    DISPATCH           = 0
    HEARTBEAT          = 1
    IDENTIFY           = 2
    PRESENCE           = 3
    VOICE_STATE        = 4
    VOICE_PING         = 5
    RESUME             = 6
    RECONNECT          = 7
    REQUEST_MEMBERS    = 8
    INVALIDATE_SESSION = 9
    HELLO              = 10
    HEARTBEAT_ACK      = 11
    GUILD_SYNC         = 12


    async def recv_msg(self):
        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix:
            return
        if item:
            item = self.zlib.decompress(item)
            item = json.loads(item)
            # Get op codes and events
            # Handle everything op code/event related here, don't return anything
            # I guess we kinda scrapping everything
            op = item.get("op")
            data = item.get("d")
            event = item.get("t")


            if  op == self.RECONNECT:
                await self.close()
                raise ReconnectWebsocket("Connection was closed.")
            elif op == self.INVALIDATE_SESSION:
                if data is True:
                    await self.close()
                    raise ReconnectWebsocket("Connection was closed.")

            elif op == self.HELLO:
                interval = data['heartbeat_interval'] / 1000.0
                await self.identify()
                asyncio.create_task(self.heartbeat(interval))

            elif op == self.HEARTBEAT_ACK:
                await self.heartbeat_ack()
            elif op == self.DISPATCH:
                handle = f"handle_{event.lower()}"
                if hasattr(self.handler, handle):
                    method = getattr(self.handler,handle)

                    asyncio.create_task(method(data, self.user, self.http))









    async def send_json(self, payload: dict):
        await self.ws.send(json.dumps(payload))

    async def connect(self):
        self.ws = await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream")
        self.alive = True

    async def close(self):
        self.alive= False
        await self.ws.close()

    async def identify(self):
        payload = {
            'op': 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "android",
                    "$browser": "Discord Android",
                    "$device": "Discord Android",
                    '$referrer': "",
                    '$referring_domain': ""
                },
            }
        }
        await self.send_json(payload)



    async def heartbeat(self, interval):
        await aprint(f"Hearbeat loop has began with the interval of {interval} seconds!")
        heartbeatJSON = {
            "op": 1,
            "d": time.time()
        }
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            self.last_send = time.perf_counter()
            if self.show_heartbeat:
                await aprint("Sent Beat")

    async def heartbeat_ack(self):
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send



    async def start(self, token: str, user: Client, bot):
        self.handler = EventHandler(bot, self.http)
        self.bot = bot
        await self.bot._help()
        self.user = user
        self.token = token
        await self.connect()
        while self.alive:
            try:
                await self.recv_msg()
            except KeyboardInterrupt:
                await aprint("Shutting down...")
                await self.close()
            except Exception as e:
                await aprint(e)
                await self.close()
















