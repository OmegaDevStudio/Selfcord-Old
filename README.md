# Selfcord
A discord selfbot API wrapper (WIP)


Example usage:

```python
import selfcord

token = "insert token"
bot = selfcord.Bot(prefixes=["!"])

@bot.on("ready")
async def ball(time):
    print(f"Connected To {bot.user.name}")

@bot.cmd(description = "Hi", aliases = ["hello"])
async def hi(ctx):
    await ctx.reply("Hi")

@bot.cmd()
async def delete(ctx):
    await ctx.message.delete()

@bot.on("message_create")
async def reply(message):
    if message.content == "Hi":
        await message.channel.send("hi")

bot.run(token)
```
