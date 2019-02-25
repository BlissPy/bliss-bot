import string
import random

from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"{ctx.author.mention}, 🏓 {round(self.bot.latency*1000, 2)}ms")

    @commands.command(name="test", hidden=True)
    @commands.is_owner()
    async def test(self, ctx):
        m = await ctx.send("_ _")
        for _ in range(0, 15):
            m = await m.edit(content=m.content + random.choice(string.printable))


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
