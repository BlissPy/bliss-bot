from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"{ctx.author.mention}, 🏓 {round(self.bot.latency*1000, 2)}ms")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
