from discord.ext import commands


def require_player():
    async def predicate(ctx: commands.Context):
        if ctx.author.id in ctx.bot.map.players:
            return True
        return False
    return commands.check(predicate)


def lack_player():
    async def predicate(ctx: commands.Context):
        if ctx.author.id not in ctx.bot.map.players:
            return True
        return False
    return commands.check(predicate)


def is_idle():
    async def predicate(ctx: commands.Context):
        return await (ctx.bot.map.get_player(ctx.author.id)).is_traveling()
    return commands.check(predicate)
