import random

from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mock(self, ctx, *, phrase: commands.clean_content = None):
        """Mock some text. If you don't supply text it will use the last message in this channel."""
        if phrase is None:
            async for message in ctx.channel.history(limit=1, before=ctx.message):
                phrase = message.content
        await ctx.send("".join(random.choice([p.upper, p.lower])() for p in phrase))


def setup(bot):
    bot.add_cog(Fun(bot))
