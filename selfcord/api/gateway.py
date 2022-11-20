import asyncio
import websockets
from aioconsole import aprint
import json
import time
import zlib
from .events import EventHandler
from .errors import ReconnectWebsocket
from selfcord.models.client import Client
import requests

class Activity:

    @staticmethod
    def Game(name, details: str="", state: str="", buttons: dict={}, application_id: str="1037788701318729799", key: str = "dolphine"):
        type = 0
        button_urls = [button for button in buttons.values()]
        buttons: list = [button for button in buttons.keys()]
        req = requests.get(f"https://discordapp.com/api/oauth2/applications/{application_id}/assets")
        for item in req.json():
    
            if item['name'] == key:
                key = item['id']

        if len(button_urls) == 0 or len(buttons) == 0:
            payload = {
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
        else:
            payload = {
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
                "created_at": int(time.time())
            }


        return payload

    @staticmethod
    def Stream(name, details: str="", state: str="", url: str="https://www.youtube.com/watch?v=CyIrJVp-sH8",buttons: dict={}, application_id: str="1037788701318729799", key: str = "dolphine"):
        type = 1
        button_urls = [button for button in buttons.values()]
        buttons: list = [button for button in buttons.keys()]
        req = requests.get(f"https://discordapp.com/api/oauth2/applications/{application_id}/assets")
        for item in req.json():

            if item['name'] == key:
                key = item['id']

        if len(button_urls) == 0 or len(buttons) == 0:
            payload = {
                "name": name,
                "details": details,
                "type": type,
                "state": state,
                "application_id": application_id,
                "assets": {
                    "large_image": key,
                },
                "created_at": int(time.time()),
                "url": url
            }
        else:
            payload = {
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
                "created_at": int(time.time())
            }

        return payload

    @staticmethod
    def Listen(name, details: str="", state: str="", buttons: dict={}, application_id: str="1037788701318729799", key: str = "dolphine"):
        type = 2
        button_urls = [button for button in buttons.values()]
        buttons: list = [button for button in buttons.keys()]
        req = requests.get(f"https://discordapp.com/api/oauth2/applications/{application_id}/assets")
        for item in req.json():

            if item['name'] == key:
                key = item['id']

        if len(button_urls) == 0 or len(buttons) == 0:
            payload = {
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
        else:
            payload = {
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
                "created_at": int(time.time())
            }


        return payload
    @staticmethod
    def Watch(name, details: str="", state: str="", buttons: dict={}, application_id: str="1037788701318729799", key: str = "dolphine"):
        type = 3

        button_urls = [button for button in buttons.values()]
        buttons: list = [button for button in buttons.keys()]

        req = requests.get(f"https://discordapp.com/api/oauth2/applications/{application_id}/assets")
        for item in req.json():

            if item['name'] == key:
                key = item['id']

        if len(button_urls) == 0 or len(buttons) == 0:
            payload = {
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
        else:
            payload = {
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
                "created_at": int(time.time())
            }


        return payload



class gateway:
    ''' OP CODES '''
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

    def __init__(self, http, show_heartbeat=False):
        self.show_heartbeat = show_heartbeat
        self.http = http
        self.zlib = zlib.decompressobj()
        self.zlib_suffix = b'\x00\x00\xff\xff'
        self.last_ack = time.perf_counter()
        self.last_send = time.perf_counter()
        self.latency = float('inf')
        self.alive = False

    async def recv_msg(self):
        '''
        Receives Message from gateway, encodes as json and does things depending on op code

        '''
        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix: return

        if item:
            item    = self.zlib.decompress(item)
            item    = json.loads(item) # Get json message from gateway

            op      = item.get('op') # Op code
            data    = item.get('d') # Data
            event   = item.get('t') # The event


            if  op == self.RECONNECT:
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

                if hasattr(self.handler, handle): # If the event handler exists, so e.g handle_ready
                    method = getattr(self.handler,handle)

                    val = await asyncio.gather(asyncio.create_task(method(data, self.user, self.http)), return_exceptions=True) # A background task is created to run the handler
                    for item in val:
                        if item == None: break
                        else: await self.bot.emit('error', item)

                    # asyncio.create_task(method(data, self.user, self.http))
                # Handlers are all situated in events.py


    def roundup(self, n):
        import math
        return int(math.ceil(n / 100.0)) * 100

    def chunks(self, lst, n):
        for i in range(0, len(lst), 1):
            if len(lst[:i+1]) > 3:
                for i in range(i, len(lst), n): yield lst[i:i + n]
                break

            yield lst[:i+1]

    async def change_presence(self, status: str, afk: bool=False, activity: dict= Activity.Game("Selfcord", "Greatest wrapper" )):
        """Change the clients current presence

        Args:
            status (str): online, offline or dnd
            afk (bool): Whether client is set as AFK
            activity (Activity): Activity object
        """
        payload = {
            "op": 3,
            "d" : {
                "since": time.time(),
                "activities": [activity],
                "status": status.lower(),
                "afk": afk
            },
        }

        await self.send_json(payload)



    async def lazy_chunk(self, guild_id: str, channel_id: str, amount: int):
        '''Sends lazy guild request to gather current online members

        Args:
            guild_id (str): The guild id specified
            channel_id (str): The channel id specified
        '''

        ranges = []

        for i in range(0, amount, 100):
            ranges.append([i, self.roundup(i + (amount - i)) - 1]) if i + 99 > amount else ranges.append([i, i+99])

        for item in self.chunks(ranges, 3):
            payload = {
                'op': 14,
                'd': {
                    'guild_id': guild_id,
                    'typing': True,
                    'channels': {channel_id:item}
                }
            }

            await self.send_json(payload)


    async def send_json(self, payload: dict):
        '''Send json to the gateway

        Args:
            payload (dict): Valid payload to send to the gateway
        '''
        await self.ws.send(json.dumps(payload))

    async def connect(self):
        '''Connect to discord gateway
        '''
        self.ws = await websockets.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream', origin='https://discord.com')
        self.alive = True

    async def close(self):
        '''Close the connection to discord gateway
        '''
        self.alive= False
        await self.ws.close()

    async def identify(self):
        '''Identify to gateway, uses amazing mobile client spoof
        '''
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



    async def heartbeat(self, interval):
        '''Heartbeat for gateway to maintain connection

        Args:
            interval (int): Interval between sends
        '''
        await aprint(f'Hearbeat loop has began with the interval of {interval} seconds!')
        heartbeatJSON = {
            'op': 1,
            'd': time.time()
        }
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            self.last_send = time.perf_counter()
            if self.show_heartbeat:
                await aprint('Sent Beat')

    async def heartbeat_ack(self):
        '''Whenever heartbeat ack is sent, logs the time between last send of heartbeat json and receive of the ack
        '''
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send

    async def start(self, token: str, user: Client, bot):
        '''Start discord gateway connection

        Args:
            token (str): User token
            user (Client): User client
            bot (_type_): Bot class
        '''
        self.handler = EventHandler(bot, self.http)
        self.bot = bot

        await self.bot.inbuilt_commands() # In built commands very cool

        self.user = user
        self.token = token

        await self.connect()
        while self.alive:
            try: await self.recv_msg()
            except KeyboardInterrupt:
                await aprint('Shutting down...')
                await self.close()
            except Exception as e:
                await self.bot.emit('error', e)
                await self.close()

    async def ring(self, channel, guild=None):
        payload = {
            "op": 4,
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
        await self.http.request(method="post", endpoint=f"/channels/{channel}/call/ring",json={"recipients":None})




    async def leave_call(self):
        payload = {
            "op": 4,
            "d": {
                "guild_id": None,
                "channel_id": None,
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            }
        }
        await self.send_json(payload)
















