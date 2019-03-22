from aiofiles import open as async_open

import asyncpg
from discord.ext import commands


class Database(commands.Cog, command_attrs=dict(checks=commands.is_owner)):

    def __init__(self, bot):
        self.bot = bot
        self.credentials = bot.db_credentials
        self.db = None
        bot.loop.create_task(self.setup_database())

    async def setup_database(self):
        db = await asyncpg.create_pool(**self.credentials)
        async with async_open("setup.sql") as sql:
            await db.execute(await sql.read())

        self.db = db
        self.bot.db = db

    @commands.command()
    async def execute(self, ctx, *, sql: str):
        await ctx.send("```\n" + await self.db.execute(sql) + "```")


def setup(bot):
    bot.add_cog(Database(bot))
