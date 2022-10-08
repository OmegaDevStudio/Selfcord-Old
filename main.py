from selfcord.bot import Bot
import asyncio
import json

bot = Bot()

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")

async def main():
    await bot.run(token)



asyncio.run(main())



