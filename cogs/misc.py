import time
import json
import typing

import discord
import discord.http
from discord.ext import commands


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
        """Return the bot's current ping."""
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
        """Return a channel, message, or member as a dict."""
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument("You forgot to supply a subcommand")

    @raw.command(aliases=["msg"])
    async def message(self, ctx, message_id: int):
        """Return a message as a dict."""
        message = await ctx.channel.fetch_message(message_id)
        if message is None:
            raise commands.BadArgument("Message with that ID was not found. It must be in this channel")

        raw = await ctx.bot.http.get_message(message.channel.id, message.id)

        try:
            await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))
        except discord.HTTPException:
            raw_string = "```json\n{}```".format(self._escape_codeblocks(self._format_json(raw)))
            half = int(len(raw_string) / 2)
            raw_string = [raw_string[0:half] + "```", "```json\n" + raw_string[half:len(raw_string)]]
            await ctx.send(raw_string[0])
            await ctx.send(raw_string[1])

    @raw.command(aliases=["user"])
    async def member(self, ctx, user: discord.User = None):
        """Return a member as a dict."""
        if user is None:
            user = ctx.author

        route = discord.http.Route("GET", f"/users/{user.id}")
        raw = await ctx.bot.http.request(route)

        await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))

    @raw.command()
    async def channel(self, ctx,
                      channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel] = None):
        """Return a channel as a dict."""
        if channel is None:
            channel = ctx.channel

        route = discord.http.Route("GET", f"/channels/{channel.id}")
        raw = await ctx.bot.http.request(route)

        await ctx.send("```json\n{}```".format(self._escape_codeblocks(self._format_json(raw))))

    @commands.command()
    async def source(self, ctx):
        """Send you the link to the bot's source."""
        await ctx.send("Bot Source: **<https://github.com/BlissPy/bliss-bot>**\n"
                       "Image Function Source: **<https://github.com/BlissPy/bliss-ops>**")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            if after.nick is not None:
                await self.bot.db.execute(f"INSERT INTO usernames VALUES ({after.id}, $1)", after.nick)

        if before.name != after.name:
            await self.bot.db.execute(f"INSERT INTO usernames VALUES ({after.id}, $1)", after.name)

    @commands.command()
    async def aka(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        aliases = []
        for alias in await self.bot.db.fetch("SELECT name FROM usernames WHERE userid = $1;", member.id):
            if alias != member.name and alias != member.nick:
                aliases.append([a for a in alias.values()][0])

        if aliases:
            akas = "\n".join(f"- {alias}" for alias in aliases)
        else:
            akas = "This user has no known aliases."

        embed = discord.Embed(
            title=f"{member.name}'s Aliases",
            description=akas,
            color=self.bot.color
        )
        embed.set_thumbnail(
            url=member.avatar_url_as(size=64, format="png")
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def insult(self, ctx):
        async with self.bot.http._session.get("https://evilinsult.com/generate_insult.php?lang=en&type=json") as resp:
            json = await resp.json()

        await ctx.send(json["insult"])


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
