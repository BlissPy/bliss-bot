import asyncio
from discord.ext import commands
import discord


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}
        self.bot.loop.create_task(self.setup_prefixes())
        bot.prefix = self.get_prefix

    async def get_prefix(self, bot, message):
        return commands.when_mentioned_or(self.prefixes[message.guild])(bot, message)

    async def setup_prefixes(self):
        await self.bot.wait_until_ready()
        if self.bot.db is not None:
            for guild in self.bot.guilds:
                self.prefixes.setdefault(guild.id, ["bl "])

            for guild_id, prefixes in await self.bot.db.fetch("SELECT * FROM prefixes;"):
                self.prefixes[guild_id].append(prefixes)

    async def export_to_db(self):
        await self.bot.db.execute("DROP TABLE prefixes;")
        await self.bot.db.execute("""CREATE TABLE IF NOT EXISTS prefixes (
guildid BIGINT PRIMARY KEY,
prefix VARCHAR(32)[] NOT NULL
);""")
        for guild in self.bot.guilds:
            p = self.prefixes.get(guild.id, ["bl "])
            await self.bot.db.execute(f"INSERT INTO prefixes VALUES ({guild.id}, $1);", p)

    @commands.Cog.listener("on_guild_join")
    async def add_new_guild(self, guild):
        self.prefixes.setdefault(guild.id, ["bl "])

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix_list = "\n".join(f"\"{prefix}\"" for prefix in self.prefixes[ctx.guild.id])
            embed = discord.Embed(
                title=f"{ctx.guild.name}'s Prefixes",
                description=prefix_list,
                color=self.bot.color
            )
            await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_server=True)
    async def add(self, ctx, prefix: str):
        if len(prefix) > 32:
            raise commands.BadArgument("Your prefix must be less than 32 characters.")

        self.prefixes[ctx.guild.id].append(prefix)

        embed = discord.Embed(
            title=f"Prefix Added To{ctx.guild.name}",
            description=f"You can now use `{prefix}` to call me!",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_server=True)
    async def remove(self, ctx, prefix: str):
        guild_prefixes = self.prefixes[ctx.guild.id]
        prefix = guild_prefixes.pop(guild_prefixes.index(prefix))

        embed = discord.Embed(
            title="Prefix Removed",
            description=f"You can no longer use `{prefix}` to call me.",
            color=self.bot.color
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))
