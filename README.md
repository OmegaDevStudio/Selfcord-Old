# Selfcord
A discord selfbot API wrapper (WIP)

## Installation

Run this in the command line.
```
pip install selfcord.py
```

## Wiki

Read our [Wiki](https://github.com/Shell1010/Selfcord/wiki) in regards to documentation and getting started.

## Examples

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

Please join our [discord server](https://discord.gg/W5QMKHejQB) here.