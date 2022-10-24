import pytest
import selfcord

bot = selfcord.Bot(prefixes=["!"])

@pytest.mark.asyncio
class Tests:
    async def test(*args):
        print("HELLO WORLD", args)


    try:
        bot.add_cmd(coro=test, description="Sends hello!", aliases=["hello"])
    except Exception as e:
        raise RuntimeError(f"Failed to add command. Error: {e}")

    cmds = len(bot.commands)
    print(cmds)
    assert cmds > 0