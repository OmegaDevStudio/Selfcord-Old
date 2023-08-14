import os

import pytest

import selfcord

bot = selfcord.Bot(prefixes=["!"])

@pytest.mark.asyncio
class Test_extension_test:
    def load_test(self):
        try:
            for item in os.listdir("./exts"):
                bot.load_extension(name=f"{item[:-3]}")
        except Exception as e:
            raise RuntimeError(f"Could not load extension. Error: {e}")

        exts = len(bot.extensions)
        assert exts > 0


@pytest.mark.asyncio
class Test_command_test:
    async def test(self, *args):
        return "HELLO WORLD"

    def add_cmd_test(self):
        try:
            bot.add_cmd(coro=self.test, description="Sends hello!", aliases=["hello"])
        except Exception as e:
            raise RuntimeError(f"Failed to add command. Error: {e}")

        cmds = len(bot.commands)
        assert cmds > 0

