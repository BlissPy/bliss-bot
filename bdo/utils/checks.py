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
