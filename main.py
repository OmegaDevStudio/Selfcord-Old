import selfcord
import json
import sys
from aioconsole import aprint

from selfcord.models import message


sys.dont_write_bytecode = True

bot = selfcord.Bot(prefixes=["!", "o!"])

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")



@bot.on("ready")
async def ball(time):
    print(f"{bot.user.name}\nTook {time * 1000:2f}ms to start up")

# @bot.on("message_create")
# async def commands(message):
#     if message.content.startswith("discord.gg"):
#         await aprint(message.content)

@bot.cmd(description="The help command", aliases=["help"])
async def test(ctx):
    await ctx.message.delete()
    msg = f"```\n"
    msg += f"{bot.user} selfbot\n"
    for command in bot.commands:
        msg += f"{command.name}:    {command.description}\n"
    msg += f"```"
    await ctx.send(f"{msg}")

@bot.cmd(description="Spams messages")
async def spam(ctx, amount: int, message: str) :
    await ctx.message.delete()
    for i in range(int(amount)):
        await ctx.send(f"{message}")



bot.run(token)


