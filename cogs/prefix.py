import asyncio

from discord.ext import commands
import discord


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}
        self.bot.loop.create_task(self.import_db())

    async def import_db(self):
        tries = 0
        while True:
            if self.bot.db is not None:
                for guild_id, prefix in await self.bot.db.fetch("SELECT * FROM prefixes;"):
                    if self.bot.get_guild(guild_id) is not None:
                        self.prefixes.update({guild_id: prefix})
                return
            elif tries > 30:
                print("Failed to load Database for prefixes.")
            else:
                await asyncio.sleep(1)
                tries += 1

    async def export_db(self):
        for guild_id, prefix in self.prefixes.items():
            await self.bot.db.execute("INSERT INTO prefixes VALUES ($1, $2)", guild_id, prefix)
            return await self.bot.db.execute("DELETE FROM prefixes;")

    @commands.group()
    async def prefix(self, ctx):
        """View the current prefix. Sub-commands include set prefix and reset prefix."""
        if ctx.invoked_subcommand is None:
            prefix = self.prefixes.get(ctx.guild.id, self.bot.default_prefix)
            embed = discord.Embed(
                name=f"{ctx.guild.name}'s Prefix",
                description=f"The prefix in this server is \"{prefix}\".",
                color=self.bot.color
            )
            await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_server=True)
    async def set(self, ctx, prefix: str):
        """Set the prefix for the server."""
        self.prefixes.update({ctx.guild.id: prefix.lower()})
        embed = discord.Embed(
            name=f"Prefix Updated",
            description=f"You can now activate me in this server with the prefix \"{prefix.lower()}\".",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @prefix.command(aliases=["remove", "delete"])
    @commands.has_permissions(manage_server=True)
    async def reset(self, ctx):
        """Reset the prefix for the server."""
        old_prefix = self.prefixes.pop(ctx.guild.id)
        embed = discord.Embed(
            title="Prefix Reset",
            description=f"""\"{old_prefix}\" will no longer work in this server.
            You are now using the default prefix, \"{self.bot.default_prefix}\".""",
            color=self.bot.color
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))
