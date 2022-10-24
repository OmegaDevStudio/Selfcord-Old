import selfcord

bot = selfcord.Bot(prefixes=["!"])


async def test():
    print("HELLO WORLD")


try:
    bot.add_cmd(coro=test, description="Sends hello!", aliases=["hello"])
except Exception as e:
    raise RuntimeError(f"Failed to add command. Error: {e}")

    