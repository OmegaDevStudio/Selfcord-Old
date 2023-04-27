import pytest
import selfcord

bot = selfcord.Bot(prefixes=["!"])

@pytest.mark.asyncio
class Tests:
    async def test(self, *args):
        return "HELLO WORLD"

    def add_cmd_test(self):
        try:
            bot.add_cmd(coro=self.test, description="Sends hello!", aliases=["hello"])
        except Exception as e:
            raise RuntimeError(f"Failed to add command. Error: {e}")

        cmds = len(bot.commands)
        assert cmds > 0





