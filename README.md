# Selfcord
A discord selfbot API wrapper (WIP)


Example usage:

```python
import selfcord

token = "token"
bot = selfcord.Bot(prefixes=["!"])

@bot.on("ready")
async def ball(time):
    print(f"{bot.user.name}\nTook {time * 1000:2f}ms to start up")

@bot.on("message_create")
async def commands(message):
    if message.content.startswith("discord.gg"):
        await aprint(message.content)

@bot.cmd(description="ping pong", aliases=["test"])
async def ping(ctx):
    await ctx.send(f"pong!")


bot.run(token)
```
