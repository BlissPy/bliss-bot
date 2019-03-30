import random

from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mock(self, ctx, *, phrase: commands.clean_content = ""):
        """Mock some text. If you don't supply text it will use the last message in this channel."""
        limit = 0
        while phrase == "":
            limit += 1
            messages = await ctx.channel.history(limit=limit, before=ctx.message).flatten()
            message = messages[len(messages)-1]
            phrase = message.clean_content
        await ctx.send("".join(random.choice([p.upper, p.lower])() for p in phrase))

    @commands.command(hidden=True)
    async def bl(self, ctx):
        await ctx.send("bl bl bl")


def setup(bot):
    bot.add_cog(Fun(bot))
