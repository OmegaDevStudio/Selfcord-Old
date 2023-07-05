"""Where Selfcord interacts with discords API directly, using discord gateway (websockets) and http requests. This is also where events are located."""
from .gateway import Activity, gateway
from .http import http
from .voice import *
