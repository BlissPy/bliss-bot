import os
import traceback

import discord
from discord.ext import commands


# noinspection PyBroadException
class Bot(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=self.prefix, *args, **kwargs)
        self.db = None
        self.redis = None

        self.color = discord.Color.from_rgb(
            254, 202, 87
        )
        self.owners = [
            217462890364403712
        ]
        self.initial_cogs = [
            "jishaku",
            "cogs.image",
            "cogs.misc",
            "cogs.errorhandler",
            "cogs.database",
            "cogs.prefix",
            "cogs.fun",
            "cogs.redis",
            "bdo.cog"
        ]
        self.default_prefix = "bl "
        self.db_credentials = {
            "host": "127.0.0.1",
            "password": "zanebot",
            "database": "zanebase",
            "user": "zane"
        }

        self.is_accepting_commands = False

    async def prefix(self, bot, message):
        if "Prefix" in self.cogs:
            custom_prefix = self.cogs["Prefix"].prefixes.get(message.guild.id, bot.default_prefix)
            return commands.when_mentioned_or(*{bot.default_prefix, custom_prefix})(bot, message)
        return commands.when_mentioned_or(bot.default_prefix)(bot, message)

    async def on_ready(self):
        print("Initiated.")
        self.is_accepting_commands = True

    async def is_owner(self, user: discord.User):
        if user.id in self.owners:
            return True
        else:
            return False

    async def on_message(self, message):
        if not self.is_accepting_commands:
            return
        if message.author.bot:
            return
        await self.process_commands(message)

    def run(self, *args, **kwargs):
        for cog in self.initial_cogs:
            try:
                self.load_extension(cog)
            except Exception:
                print(f"Error loading {cog}; traceback printed below.")
                traceback.print_exc()
        super().run(*args, **kwargs)

    async def logout(self):
        if "Imaging" in self.cogs:
            await self.cogs["Imaging"].session.close()
        if "Prefix" in self.cogs:
            await self.cogs["Prefix"].export_db()
        print("Goodbye.")
        await self.close()


if __name__ == "__main__":
    # This will stop it from showing up in the help menu
    os.environ['JISHAKU_HIDE'] = "true"

    with open("token.txt", "r") as f:
        token = f.read()
    Bot(status=discord.Status.dnd).run(token)
