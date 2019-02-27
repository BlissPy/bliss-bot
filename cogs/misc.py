import string
import random

import discord
from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Ping",
            description=f"🏓 {round(self.bot.latency*1000, 2)}ms",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
