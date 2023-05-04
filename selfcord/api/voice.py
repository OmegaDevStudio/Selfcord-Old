from __future__ import annotations
import asyncio
import websockets
from aioconsole import aprint
import json
import time
import zlib
from selfcord.models.client import Client
import requests
from traceback import format_exception


class Voice:
    def __init__(self, session_id: str, token: str, endpoint: str) -> None:
        self.session_id = session_id
        self.token = token
        self.endpoint = endpoint

