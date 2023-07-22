<div align="center">
<img src="./logo.png" widht="180" height="180" style="border-radius: 100%;">
<h1 align="center">SELFCORD</h1>
<strong><i>A Powerful Library for Discord Selfbots</i></strong>
<br>
<br>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/MADE%20WITH-PYTHON-red?logoColor=red&logo=Python&style=for-the-badge">
</a>
<a href="https://pypi.org/project/selfcord/">
<img src="https://img.shields.io/badge/version-0.2.4-blue?logo=adguard&style=for-the-badge">
</a>
<a href="https://github.com/Shell1010/Selfcord/wiki">
<img src="https://img.shields.io/badge/documentation-green?logo=gitbook&style=for-the-badge">
</a>
</div>

## Feautres
 - Modern Pythonic API using `async`/`await` syntax
 - Easy to use with an object oriented design
 - Optimised for both speed and memory
 - Prevents detection of user account automation
 - Clean Documentation
 - Community Support

## Installation
Python 3.10 or higher is required.
```
pip install selfcord.py
```

## Wiki

Read our [Wiki](https://github.com/Shell1010/Selfcord/wiki) in regards to documentation and getting started.

## Getting Started
A selfbot that responds to a message ("ping!") with another message ("pong").
```py
import selfcord

token = "insert token"
bot = selfcord.Bot()

@bot.on("ready")
async def ready(time):
    print(f"Connected To {bot.user.name}\n Startup took {time:0.2f} seconds")

@bot.on("message")
async def responder(message):
    if message.content == "ping!":
        await message.channel.send("pong!")

bot.run(token)
```
## Examples/Usage
### Message logger
In this snippet, If someone deletes messages in the server, it records details such as the server name, channel name, message content, and the author's name
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
In this snippet, you are able to delete certain amount of messages from a channel
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
In this snippet, you can retrieve the most recently deleted message.
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
## Some Useful Links
- [Documentation](https://github.com/Shell1010/Selfcord/wiki)
- [Other Documentation (messy)](https://github.com/Shell1010/Selfcord/tree/main/docs)
- [PyPi](https://pypi.org/project/selfcord.py/)
- [Official Discord Server](https://discord.gg/FCFnnBGzkg)
- [A simple selfbot designed to showcase the library's features](https://github.com/Shell1010/Aeterna-Selfbot)

## Contributing
Contributors are always Welcome
