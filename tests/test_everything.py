import selfcord
import json
from aioconsole import aprint



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

@bot.on("message_delete")
async def message_logger(message):
    # DISCLAIMER: If message is not in bots cache only message id, channel id and guild id will be present
    if message.author != None:
        if message.author.id != bot.user.id:
            print(message.author.id, bot.user.id)
            if message.guild != None:
                await aprint(f"""MESSAGE LOGGED:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
CONTENT:
{message.author}: {message.content}
""")
            else:
                await aprint(f"""MESSAGE LOGGED:
    CHANNEL: {message.channel}
    CONTENT:
    {message.author}: {message.content}
                """)

@bot.on("error")
async def error_logger(error):
    await aprint(f"ERROR: {error}")

@bot.on("message_create")
async def invite_logger(message):
    if "discord.gg/" in message.content:
        await aprint(f"{message.content}")


@bot.cmd(description="Displays the latency of the gateway", aliases=["ping"])
async def latency(ctx):
    await ctx.reply(f"```diff\n+ Ping is {bot.latency * 1000:0.2f}ms```")

@bot.cmd(description="Check roles", aliases=["allroles"])
async def roles(ctx):
    msg = "```diff\n"
    for role in ctx.guild.roles:
        msg += f"+ {role.name}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="Spams messages")
async def spam(ctx, amount: int, *, message: str) :
    await ctx.message.delete()
    await ctx.spam(amount, message)

@bot.cmd(description="Checks emojis")
async def emojis(ctx):
    msg = "```diff\n"
    for emoji in ctx.guild.emojis:
        msg += f"+ {emoji.name}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="Check channels", aliases=["allchans"])
async def channels(ctx):
    msg = "```diff\n"
    for channel in ctx.guild.channels:
        msg += f"+ {channel.name}\n"
    msg += "```"
    await ctx.reply(msg)

@bot.cmd(description="User information", aliases=["userinfo"])
async def whois(ctx, id: str):
    msg = "```diff\n"
    user = await bot.get_user(id)
    msg += f"- Username: {user}\n- ID: {user.id}\n- Bot?: {user.bot}\n- Created At: {user.timestamp}```"
    avatar = user.avatar_url
    banner = user.banner_url
    msg += f"AVATAR: {avatar}\nBANNER: {banner}"
    await ctx.reply(msg)

@bot.cmd(description="Adds users as friends", aliases=["addfriend"])
async def friend(ctx, id: str):
    await bot.add_friend(id)
    await ctx.reply("Successfully sent request!")

@bot.cmd(description="Category create")
async def category(ctx):
    for i in range(5):
        await ctx.guild.category_channel_create("balls")

@bot.cmd(description="Edit guild")
async def editguild(ctx, icon=None):
    await ctx.message.delete()
    await ctx.guild.edit(icon_url=icon)

@bot.cmd(description="Edit profile")
async def editprofile(ctx):
    await ctx.message.delete()
    await bot.edit_profile(bio="Writing a discord wrapper...", accent=123456)

@bot.cmd(description="Spams channels", aliases=["chanspam"])
async def cc(ctx, amount: int, *, message: str):
    await ctx.message.delete()
    for i in range(amount):
        await ctx.guild.txt_channel_create(message)

@bot.cmd(description="Steals a users pfp", aliases=['getpfp'])
async def stealpfp(ctx, id: str):
    user = await bot.get_user(id)
    await bot.change_pfp(user.avatar_url)
    await ctx.reply("Successfully stole da pfp")

@bot.cmd(description="Purge messages", aliases=['clear'])
async def purge(ctx, amount: int =None):
    await ctx.purge(int(amount))


bot.run(token)

