import random

from discord.ext import commands


class Fun(commands.Cog):

    OWO_MAP = {
        "o": "owo",
        "r": "w",
        "ll": "y",
        "O": "OwO",
        "R": "Ww",
        "Ll": "Y",
        "LL": "Y"
    }

    def __init__(self, bot):
        self.bot = bot

    async def get_last_content(self, before, channel):
        phrase = ""
        limit = 0
        while phrase == "":
            if limit > 5:
                return None
            limit += 1
            messages = await channel.history(limit=limit, before=before).flatten()
            message = messages[len(messages) - 1]
            phrase = message.clean_content
        return phrase

    @commands.command()
    async def mock(self, ctx, *, phrase: commands.clean_content = None):
        """Mock some text. If you don't supply text it will use the last message in this channel."""
        if phrase is None:
            phrase = await self.get_last_content(ctx.message, ctx.channel)

        if phrase is None:
            await ctx.send("Not enough content in channel.")

        await ctx.send("".join(random.choice([p.upper, p.lower])() for p in phrase))

    @commands.command()
    async def owo(self, ctx, *, phrase: commands.clean_content = None):
        """Mock some text. If you don't supply text it will use the last message in this channel."""
        if phrase is None:
            phrase = await self.get_last_content(ctx.message, ctx.channel)

        if phrase is None:
            await ctx.send("Not enough content in channel.")

        await ctx.send("".join(p.replace(p, self.OWO_MAP.get(p, p)) for p in phrase))

    @commands.command(hidden=True)
    async def bl(self, ctx):
        await ctx.send("bl bl bl")


def setup(bot):
    bot.add_cog(Fun(bot))
