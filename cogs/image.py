import io
import copy
import typing
import aiohttp

import discord
from discord.ext import commands

import blissops as imageops


class ImageCommand(commands.Command):

    def __init__(self, *args, **kwargs):
        self.cache_images = kwargs.get("cache", False)
        self.avatar_size = kwargs.get("avatar_size", 256)
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

    async def avatar_bytes(self, command: ImageCommand, member: discord.Member):
        async with self.session.get(member.avatar_url_as(format="png", size=command.avatar_size)) as get:
            return io.BytesIO(await get.read())

    async def add_to_cache(self, command_name, img_bytes, member):
        self.cache[command_name].update({member.avatar_url: img_bytes})

    async def from_cache(self, command_name, member):
        if member.avatar_url in self.cache[command_name]:
            return copy.deepcopy(self.cache[command_name][member.avatar_url])
        return None

    @commands.Cog.listener()
    async def on_ready(self):
        for command in self.walk_commands():
            if command.cache_images:
                self.cache.update({command.name: {}})

    @commands.command(cls=ImageCommand, cache=True, name="magic")
    async def magic(self, ctx, *, member: discord.Member = None):
        """Content aware scale a member's avatar into another planet."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.magic(b)
            f = discord.File(img, filename="generated.png")
            await self.add_to_cache(ctx.command.name, f, member)
        else:
            img = cached
            f = discord.File(img, filename="generated.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="deepfry", avatar_size=512)
    async def deepfry(self, ctx, *, member: discord.Member = None):
        """Deepfry a member's avatar. It still needs more jpeg."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.deepfry(b)
            f = discord.File(img, filename="generated.png")
            await self.add_to_cache(ctx.command.name, f, member)
        else:
            img = cached
            f = discord.File(img, filename="generated.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="emboss")
    async def emboss(self, ctx, *, member: discord.Member = None):
        """Emboss a member's avatar,"""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.emboss(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="emboss.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="vaporwave", avatar_size=512)
    async def vaporwave(self, ctx, *, member: discord.Member = None):
        """vvvaaapppooorrrwwwaaavvveee"""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.vaporwave(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="vaporwave.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="floor", avatar_size=128)
    async def floor(self, ctx, *, member: discord.Member = None):
        """The floor is lava and the lava is a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.floor(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="floor.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="concave")
    async def concave(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a concave lens."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.concave(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="concave.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="convex")
    async def convex(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a convex lens."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.convex(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="convex.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="invert", avatar_size=1024)
    async def invert(self, ctx, *, member: discord.Member = None):
        """Invert a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.invert(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="invert.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="desat")
    async def desat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Desaturate a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.desat(b, threshold)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="desat.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sat")
    async def sat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Saturate a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.sat(b, threshold)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="sat.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="lsd")
    async def lsd(self, ctx, *, member: discord.Member = None):
        """Take some LSD and look at a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.lsd(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="lsd.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="posterize")
    async def posterize(self, ctx, *, member: discord.Member = None):
        """Posterize a member's avatar,"""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.posterize(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="posterize.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="grayscale", aliases=["greyscale"], avatar_size=512)
    async def grayscale(self, ctx, *, member: discord.Member = None):
        """Grayscale a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.grayscale(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="grayscale.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="bend")
    async def bend(self, ctx, *, member: discord.Member = None):
        """Bend a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.bend(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="bend.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="edge")
    async def edge(self, ctx, *, member: discord.Member = None):
        """Make a member's avatar sharp and edgy."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.edge(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="edge.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="gay")
    async def gay(self, ctx, *, member: discord.Member = None):
        """Make someone gay. Use at your own discretion."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.gay(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="gay.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sort")
    async def sort(self, ctx, *, member: discord.Member = None):
        """Sort the pixels of a member's avatar. Makes a pretty gradient most of the time."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.sort(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="sort.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sobel")
    async def sobel(self, ctx, *, member: discord.Member = None):
        """Sobel filter a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.sobel(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="sobel.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="shuffle")
    async def shuffle(self, ctx, *, member: discord.Member = None):
        """Shuffle the pixels in a member's avatar."""
        if member is None:
            member = ctx.author

        cached = await self.from_cache(ctx.command.name, member)
        if cached is None:
            b = await self.avatar_bytes(ctx.command, member)
            img = await imageops.shuffle(b)
            await self.add_to_cache(ctx.command.name, img, member)
        else:
            img = cached
        f = discord.File(img, filename="shuffle.png")

        embed = discord.Embed(
            title=f"{ctx.command.name.upper()} | {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        embed.set_image(url="attachment://generated.png")

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=False, name="ascii")
    async def ascii_art(self, ctx, *, member: discord.Member = None):
        """Make ascii-art out of a member's avatar."""
        if member is None:
            member = ctx.author

        async with ctx.typing():
            b = await self.avatar_bytes(ctx.command, member)
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
