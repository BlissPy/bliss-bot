import time
import asyncio
import traceback

import aioredis
from discord.ext import commands


class Redis(commands.Cog):

    REDIS_ADDRESS = "redis://127.0.0.1:42069"

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.setup_redis())

    async def setup_redis(self):
        redis = await asyncio.wait_for(aioredis.create_pool(self.REDIS_ADDRESS), timeout=420.420)
        self.bot.redis = redis
        return redis
        
    @commands.command(name="redis")
    @commands.is_owner()
    async def redis(self, ctx, method: str, *redis_args):
        try:
            start = time.perf_counter()
            out = await self.bot.redis.execute(method, *redis_args)
            duration = (time.perf_counter() - start) * 1000.0
        except:
            return await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        
        await ctx.send(f"*{round(duration, 2)}ms:* `{out}`")


def setup(bot):
    bot.add_cog(Redis(bot))
