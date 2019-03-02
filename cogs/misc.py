import time
import json
import typing

import discord
import discord.http
from discord.ext import commands


class Miscellaneous(commands.Cog):

    @staticmethod
    def _format_json(string: str):
        return json.dumps(string, indent=2, ensure_ascii=False, sort_keys=True)

    @staticmethod
    def _escape_codeblocks(line):
        if not line:
            return line

        i = 0
        n = 0
        while i < len(line):
            if (line[i]) == '`':
                n += 1
            if n == 3:
                line = line[:i] + '\u200b' + line[i:]
                n = 1
                i += 1
            i += 1

        if line[-1] == '`':
            line += '\u200b'

        return line

    @commands.command(name="ping", aliases=['ms'])
    async def _ping_command(self, ctx):
        """
        Return the bot's current ping.
        """
        ws = round(ctx.bot.latency * 1000, 2)
        a = time.perf_counter()
        msg = await ctx.send(".")
        b = time.perf_counter()
        z = b - a
        await msg.edit(content="..")
        c = time.perf_counter()
        y = b - a
        await msg.edit(content="...")
        d = time.perf_counter()
        x = c - d
        await msg.delete()
        rtt = round(sum([z*1000, y*1000, x*1000]))
        m = time.perf_counter()
        await ctx.trigger_typing()
        rsp = round((time.perf_counter() - m)*1000)

        e = discord.Embed(
            title="Ping",
            color=ctx.bot.color
        )
        e.set_thumbnail(
            url=ctx.me.avatar_url_as(static_format="png", size=64)
        )
        e.add_field(
            name="Web Socket",
            value=f"{ws}ms",
            inline=False
        )
        e.add_field(
            name="Round Trip",
            value=f"{rtt}ms",
            inline=False
        )
        e.add_field(
            name="Response Time",
            value=f"{rsp}ms",
            inline=False
        )

        await ctx.send(embed=e)

    @commands.group()
    async def raw(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument("You forgot to supply a subcommand")

    @raw.command(aliases=["msg"])
    async def message(self, ctx, message_id: int):
        message = await ctx.channel.get_message(message_id)
        if message is None:
            raise commands.BadArgument("Message with that ID was not found. It must be in this channel")

        raw = await ctx.bot.http.get_message(message.channel.id, message.id)

        await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))

    @raw.command(aliases=["user"])
    async def member(self, ctx, user: discord.User):
        raw = await ctx.bot.http.get_user_info(user.id)
        await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))

    @raw.command()
    async def channel(self, ctx,
                      channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel] = None):
        if channel is None:
            channel = ctx.channel

        route = discord.http.Route("GET", f"/channels/{channel.id}")
        raw = await ctx.bot.http.request(route)

        await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))


def setup(bot):
    bot.add_cog(Miscellaneous())
