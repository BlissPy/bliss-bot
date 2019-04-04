import asyncio

import aioredis
from discord.ext import commands


class Redis(commands.Cog):

    REDIS_ADDRESS = "127.0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.redis = None
        bot.loop.create_task(self.setup_redis())

    async def setup_redis(self):
        self.redis = await asyncio.wait_for(aioredis.create_pool(self.REDIS_ADDRESS), timeout=420.420)


def setup(bot):
    bot.add_cog(Redis(bot))
