from selfcord.bot import Bot
import asyncio
import json
import sys

sys.dont_write_bytecode = True

bot = Bot(show_beat=True)

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")

bot.run(token)







