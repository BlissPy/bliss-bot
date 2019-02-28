import io
import typing
import aiohttp

import discord
from discord.ext import commands

import imageops


class Imaging(commands.Cog, name="Image Manipulation"):

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.http._session

    async def avatar_bytes(self, member: discord.Member):
        async with self.session.get(member.avatar_url_as(format="png")) as get:
            return io.BytesIO(await get.read())

    @commands.command(name="magic")
    async def magic(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.magic(b)
        f = discord.File(img, filename="magic.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="deepfry")
    async def deepfry(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.deepfry(b)
        f = discord.File(img, filename="deepfry.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="emboss")
    async def emboss(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.emboss(b)
        f = discord.File(img, filename="emboss.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="vaporwave")
    async def vaporwave(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.vaporwave(b)
        f = discord.File(img, filename="vaporwave.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="floor")
    async def floor(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.floor(b)
        f = discord.File(img, filename="floor.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="concave")
    async def concave(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.concave(b)
        f = discord.File(img, filename="concave.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="convex")
    async def convex(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.convex(b)
        f = discord.File(img, filename="convex.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="invert")
    async def invert(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.invert(b)
        f = discord.File(img, filename="invert.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="desat")
    async def desat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.desat(b, threshold)
        f = discord.File(img, filename="desat.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="sat")
    async def sat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sat(b, threshold)
        f = discord.File(img, filename="sat.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="lsd")
    async def lsd(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.lsd(b)
        f = discord.File(img, filename="lsd.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="posterize")
    async def posterize(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.posterize(b)
        f = discord.File(img, filename="posterize.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="grayscale")
    async def grayscale(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.grayscale(b)
        f = discord.File(img, filename="grayscale.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="bend")
    async def bend(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.bend(b)
        f = discord.File(img, filename="bend.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="edge")
    async def edge(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.edge(b)
        f = discord.File(img, filename="edge.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="gay")
    async def gay(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.gay(b)
        f = discord.File(img, filename="gay.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="sort")
    async def sort(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sort(b)
        f = discord.File(img, filename="sort.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="straight")
    async def straight(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.straight(b)
        f = discord.File(img, filename="straight.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="sobel")
    async def sobel(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sobel(b)
        f = discord.File(img, filename="sobel.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="frangi")
    async def frangi(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.frangi(b)
        f = discord.File(img, filename="frangi.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="neon", aliases=["soangi"])
    async def soangi(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.soangi(b)
        f = discord.File(img, filename="soangi.png")

        await ctx.send(content=ctx.author.mention, file=f)

    @commands.command(name="ascii")
    async def ascii_art(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with ctx.typing():
            b = await self.avatar_bytes(member)
            art = await imageops.ascii_art(b)
            try:
                async with self.session.post("https://wastebin.travitia.xyz/documents", data=art) as post:
                    key = (await post.json())["key"]
                await ctx.send(f"{ctx.author.mention}, https://wastebin.travitia.xyz/{key}.txt")
            except KeyError:
                await ctx.send("Sorry. I was able to caclulate that image but it was too large for my text-host.")
                return
            except aiohttp.ContentTypeError:
                await ctx.send("Sorry. I was able to caclulate that image but it was too large for my text-host.")
                return


def setup(bot):
    bot.add_cog(Imaging(bot))
