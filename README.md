<div align="center">
<img>
<h1 align="center">SELFCORD</h1>
<strong><i>A Powerful Library To make Discord SelfBot in Python</i></strong>
<br>
<br>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/MADE%20WITH-PYTHON-red?logoColor=red&logo=Python&style=for-the-badge">
</a>
<a href="https://ddl-api.cycno.repl.co/">
<img src="https://img.shields.io/badge/version-0.1-blue?logo=adguard&style=for-the-badge">
</a>
<a href="https://ddl-api.cycno.repl.co/">
<img src="https://img.shields.io/badge/documentation-green?logo=gitbook&style=for-the-badge">
</a>
</div>

## Installation

Run this in the command line.
```
pip install selfcord.py
```

## Wiki

Read our [Wiki](https://github.com/Shell1010/Selfcord/wiki) in regards to documentation and getting started.

## Examples

### Aeterna Selfbot

A simple selfbot designed to showcase the library's features, intended to be seen as a template or base for other users.

[Aeterna Selfbot](https://github.com/Shell1010/Aeterna-Selfbot)

### Message logger
```python
import selfcord

token = "insert token"
bot = selfcord.Bot(prefixes=["!", "?"])

@bot.on("ready")
async def ball(time):
    print(f"Connected To {bot.user}\n Startup took {time:0.2f} seconds")

@bot.on("message_delete")
async def message_logger(message):
    # DISCLAIMER: If message is not in bots cache only message id, channel id and guild id will be present
    if message.author != None:
        if message.author.id != bot.user.id:
            if message.guild != None: # If the message is in a guild
                await aprint(f"""MESSAGE LOGGED:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
CONTENT:
{message.author}: {message.content}
""")
        else: # If the message is in a DM or Group chat
            await aprint(f"""MESSAGE LOGGED:
CHANNEL: {message.channel}
CONTENT:
{message.author}: {message.content}
            """)

bot.run(token)
```
### Purge command
```python
import selfcord

token = "insert token"
bot = selfcord.Bot(prefixes=["!", "?"])

@bot.on("ready")
async def ball(time):
    print(f"Connected To {bot.user}\n Startup took {time:0.2f} seconds")

@bot.cmd(description="Purges the channel", aliases=["wipe", "clear"])
async def purge(ctx, amount: int=None):
    await ctx.purge(amount)

bot.run(token)
```

### Deleted message sniper
```python
import selfcord

token = "insert token"
bot = selfcord.Bot(prefixes=["!", "?"])

@bot.on("ready")
async def ball(time):
    print(f"Connected To {bot.user}\n Startup took {time:0.2f} seconds")

@bot.cmd(description="Snipe", aliases=['s'])
async def snipe(ctx):
    await ctx.reply(f"{bot.user.deleted_messages[-1].author}: {bot.user.deleted_messages[-1]}")

bot.run(token)
```

## Help & Support

Please join our [discord server](https://discord.gg/FCFnnBGzkg) here.
