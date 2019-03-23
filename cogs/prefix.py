from discord.ext import commands
import discord


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}


def setup(bot):
    bot.add_cog(Prefix(bot))
