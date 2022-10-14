import selfcord
import json
from aioconsole import aprint

from selfcord.models import message

bot = selfcord.Bot(prefixes=["!", "o.", "o!"])

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")



@bot.on("ready")
async def ball(time):
    await aprint(f"""
CONNECTED TO:

USER: {bot.user}
GUILDS: {len(bot.user.guilds)}
FRIENDS: {len(bot.user.friends)}

STARTUP:  {time:0.2f} seconds""")

@bot.on("message_create")
async def invite_checker(message):
    if message.content.startswith("discord.gg"):
        await aprint(message.content)



@bot.cmd(description="Displays the latency of the gateway", aliases=["ping"])
async def latency(ctx):
    await ctx.reply(f"```diff\n+ Ping is {bot.latency * 1000:0.2f}ms```")

@bot.cmd(description="Check roles", aliases=["allroles"])
async def roles(ctx):
    msg = "```diff\n"
    for role in ctx.guild.roles:
        msg += f"+{role.name}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="Spams messages")
async def spam(ctx, amount: int, *, message: str) :
    await ctx.message.delete()
    await ctx.spam(amount, message)

@bot.cmd(description="Checks emojis")
async def emojicheck(ctx):
    msg = "```diff\n"
    for emoji in ctx.guild.emojis:
        msg += f"+ {emoji.name}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="Role check")
async def rolecheck(ctx):
    msg = "```diff\n"
    for role in ctx.guild.roles:
        msg += f"+ {role.name}\n"
        msg += f"-     {role.permissions}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="Spams channels", aliases=["chanspam"])
async def cc(ctx, amount: int, *, message: str):
    await ctx.message.delete()
    for i in range(amount):
        await ctx.guild.txt_channel_create(message)





bot.run(token)


