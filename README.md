# Selfcord
A discord selfbot API wrapper (WIP)

## Installation

Run this in the command line.
```
pip install git+https://github.com/Shell1010/Selfcord.git
```


## Examples

### Base Example

```python
import selfcord

token = "insert token"
bot = selfcord.Bot(prefixes=["!", "?"])

@bot.on("ready")
async def ball(time):
    print(f"Connected To {bot.user.name}\n Startup took {time:0.2f} seconds")

@bot.cmd(description = "Hi", aliases = ["hello"])
async def hi(ctx):
    await ctx.reply("Hello!")


@bot.on("message_create")
async def reply(message):
    if message.content == "Hi":
        await message.channel.send("hi")

@bot.cmd(description="Funny spam!")
async def spam(ctx, amount: int, *, message: str):
    await ctx.message.delete()
    await ctx.spam(amount, message)

bot.run(token)
```
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

@bot.cmd(description="Does pong!")
async def ping(ctx):
    await ctx.reply("pong!")

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
```