from selfcord import Bot
import json
import sys

sys.dont_write_bytecode = True

bot = Bot(show_beat=True)

with open("./config.json", "r") as f:
    config = json.load(f)

token = config.get("token")



@bot.on("ready")
async def ready(time):
    print(f"{bot.user.name}\nTook {time * 1000:2f}ms to start up")


bot.run(token)







