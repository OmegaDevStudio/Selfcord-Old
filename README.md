# Selfcord
A discord selfbot API wrapper (WIP)

## Installation

Run this in the command line.
```
pip install selfcord
```


## Examples

Example usage:

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



