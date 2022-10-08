import asyncio
import websockets
import aioconsole
import json
import time
import struct
import socket
import zlib

class gateway:
    def __init__(self, token: str, show_heartbeat=False):
        self.show_heartbeat = show_heartbeat
        self.token = token
        self.id = None
        self.is_connected = False
        self.mode = "xsalsa20_poly1305"
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.zlib = zlib.decompressobj()
        self.zlib_suffix = b"\x00\x00\xff\xff"
        self.latency1 = None


    async def recv_json(self):
        try:
            item = await self.ws.recv()
            buffer = bytearray()
            buffer.extend(item)
            if len(item) < 4 or item[-4:] != self.zlib_suffix:
                return
            if item:
                item = self.zlib.decompress(item)
                # await aioconsole.aprint(item)
                return json.loads(item)
        except Exception as e:
            await self.simple_connect()





    async def send_json(self, payload: dict):
        await self.ws.send(json.dumps(payload))


    async def connect(self):
        self.ws = await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream")

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
        await aioconsole.aprint(f"Hearbeat loop has began with the interval of {interval} seconds!")
        heartbeatJSON = {
            "op": 1,
            "d": time.time()
        }
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            self.latency1 = time.time()
            if self.show_heartbeat:
                await aioconsole.aprint("Sent Beat")


    async def simple_connect(self):
        await self.connect()
        interval = await self.recv_json()
        await self.identify()
        asyncio.create_task(self.heartbeat(interval['d']['heartbeat_interval'] / 1000))
        event = await self.recv_json()
        if event["t"] == "READY":
            await aioconsole.aprint(f"CONNECTED AS: {event['d']['user']['username']}#{event['d']['user']['discriminator']}")
            self.id = event["d"]["user"]["id"]














