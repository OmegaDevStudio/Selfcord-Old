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

    # ALL DA OP CODES HERE
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
        """Receives Message from gateway, encodes as json and does things depending on op code

        """
        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix:
            return
        if item:
            item = self.zlib.decompress(item)
            item = json.loads(item) # Get json message from gateway

            op = item.get("op") # Op code
            data = item.get("d") # Data
            event = item.get("t") # The event


            if  op == self.RECONNECT:
                await self.close()
                raise ReconnectWebsocket("Connection was closed.")

            elif op == self.INVALIDATE_SESSION:
                if data is True:
                    await self.close()
                    raise ReconnectWebsocket("Connection was closed.")

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

                handle = f"handle_{event.lower()}"

                if hasattr(self.handler, handle): # If the event handler exists, so e.g handle_ready
                    method = getattr(self.handler,handle)

                    val = await asyncio.gather(asyncio.create_task(method(data, self.user, self.http)), return_exceptions=True) # A background task is created to run the handler
                    for item in val:
                        if item == None:
                            break
                        else:
                            await self.bot.emit("error", item)

                    # asyncio.create_task(method(data, self.user, self.http))
                # Handlers are all situated in events.py









    async def send_json(self, payload: dict):
        """Send json to the gateway

        Args:
            payload (dict): Valid payload to send to the gateway
        """
        await self.ws.send(json.dumps(payload))

    async def connect(self):
        """Connect to discord gateway
        """
        self.ws = await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream")
        self.alive = True

    async def close(self):
        """Close the connection to discord gateway
        """
        self.alive= False
        await self.ws.close()

    async def identify(self):
        """Identify to gateway, uses amazing mobile client spoof
        """
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
        """Heartbeat for gateway to maintain connection

        Args:
            interval (int): Interval between sends
        """
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
        """Whenever heartbeat ack is sent, logs the time between last send of heartbeat json and receive of the ack
        """
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send



    async def start(self, token: str, user: Client, bot):
        """Start discord gateway connection

        Args:
            token (str): User token
            user (Client): User client
            bot (_type_): Bot class
        """
        self.handler = EventHandler(bot, self.http)
        self.bot = bot
        await self.bot._help() # In built help command very cool
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
                await self.bot.emit("error", e)
















