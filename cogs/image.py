import io
import typing
import aiohttp

import discord
from discord.ext import commands

import blissops as imageops


class ImageCommand(commands.Command):

    def __init__(self, *args, **kwargs):
        self.cache_images = kwargs.get("cache", False)
        super().__init__(*args, **kwargs)


class Imaging(commands.Cog, name="Image Manipulation",
              command_attrs=dict(cooldown=commands.Cooldown(1, 3, commands.BucketType.member))):

    def __init__(self, bot):
        self.bot = bot
        self.session = None

        self.cache = {}

        bot.loop.create_task(self.create_session())

    async def create_session(self):
        self.session = aiohttp.ClientSession()

    async def avatar_bytes(self, member: discord.Member):
        async with self.session.get(member.avatar_url_as(format="png")) as get:
            return io.BytesIO(await get.read())

    async def add_to_cache(self, command_name, bytes, member):
        self.cache[command_name].update({member.avatar_url: bytes})

    @commands.Cog.listener()
    async def on_ready(self):
        for command in self.walk_commands():
            if not command.cache:
                self.cache.update({command.name: {}})

    @commands.command(cls=ImageCommand, cache=True, name="magic")
    async def magic(self, ctx, *, member: discord.Member = None):
        """Content aware scale a member's avatar into another planet."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.magic(b)
        f = discord.File(img, filename="magic.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="deepfry")
    async def deepfry(self, ctx, *, member: discord.Member = None):
        """Deepfry a member's avatar. It still needs more jpeg."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.deepfry(b)
        f = discord.File(img, filename="deepfry.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="emboss")
    async def emboss(self, ctx, *, member: discord.Member = None):
        """Emboss a member's avatar,"""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.emboss(b)
        f = discord.File(img, filename="emboss.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="vaporwave")
    async def vaporwave(self, ctx, *, member: discord.Member = None):
        """vvvaaapppooorrrwwwaaavvveee"""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.vaporwave(b)
        f = discord.File(img, filename="vaporwave.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="floor")
    async def floor(self, ctx, *, member: discord.Member = None):
        """The floor is lava and the lava is a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.floor(b)
        f = discord.File(img, filename="floor.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="concave")
    async def concave(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a concave lens."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.concave(b)
        f = discord.File(img, filename="concave.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="convex")
    async def convex(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a convex lens."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.convex(b)
        f = discord.File(img, filename="convex.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="invert")
    async def invert(self, ctx, *, member: discord.Member = None):
        """Invert a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.invert(b)
        f = discord.File(img, filename="invert.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="desat")
    async def desat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Desaturate a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.desat(b, threshold)
        f = discord.File(img, filename="desat.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sat")
    async def sat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Saturate a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sat(b, threshold)
        f = discord.File(img, filename="sat.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="lsd")
    async def lsd(self, ctx, *, member: discord.Member = None):
        """Take some LSD and look at a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.lsd(b)
        f = discord.File(img, filename="lsd.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="posterize")
    async def posterize(self, ctx, *, member: discord.Member = None):
        """Posterize a member's avatar,"""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.posterize(b)
        f = discord.File(img, filename="posterize.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="grayscale", aliases=["greyscale"])
    async def grayscale(self, ctx, *, member: discord.Member = None):
        """Grayscale a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.grayscale(b)
        f = discord.File(img, filename="grayscale.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="bend")
    async def bend(self, ctx, *, member: discord.Member = None):
        """Bend a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.bend(b)
        f = discord.File(img, filename="bend.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="edge")
    async def edge(self, ctx, *, member: discord.Member = None):
        """Make a member's avatar sharp and edgy."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.edge(b)
        f = discord.File(img, filename="edge.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="gay")
    async def gay(self, ctx, *, member: discord.Member = None):
        """Make someone gay. Use at your own discretion."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.gay(b)
        f = discord.File(img, filename="gay.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sort")
    async def sort(self, ctx, *, member: discord.Member = None):
        """Sort the pixels of a member's avatar. Makes a pretty gradient most of the time."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sort(b)
        f = discord.File(img, filename="sort.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sobel")
    async def sobel(self, ctx, *, member: discord.Member = None):
        """Sobel filter a member's avatar."""
        if member is None:
            member = ctx.author

        b = await self.avatar_bytes(member)
        img = await imageops.sobel(b)
        f = discord.File(img, filename="sobel.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url=f"attachment://{ctx.command.name}.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=False, name="ascii")
    async def ascii_art(self, ctx, *, member: discord.Member = None):
        """Make ascii-art out of a member's avatar."""
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
