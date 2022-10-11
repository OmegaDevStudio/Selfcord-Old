import selfcord
import json
import sys
from aioconsole import aprint


sys.dont_write_bytecode = True

bot = selfcord.Bot(prefixes=["!"])

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")



@bot.on("ready")
async def ball(time):
    print(f"{bot.user.name}\nTook {time * 1000:2f}ms to start up")

@bot.on("message_create")
async def commands(message):
    if message.content.startswith("discord.gg"):
        await aprint(message.content)

@bot.command(description="test", aliases=["ok"])
async def test(ctx):
    await ctx.send(f"{ctx.message.author}")


bot.run(token)


