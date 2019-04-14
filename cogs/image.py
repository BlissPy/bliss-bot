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
        bot.loop.create_task(self.generate_cache_structure())

    async def create_session(self):
        self.session = aiohttp.ClientSession()

    async def avatar_bytes(self, command: ImageCommand, member: discord.Member):
        async with self.session.get(str(member.avatar_url_as(format="png", size=command.avatar_size))) as get:
            return io.BytesIO(await get.read())

    async def add_to_cache(self, command, img_bytes, member):
        self.cache[command.name].update({member.avatar_url: copy.deepcopy(img_bytes)})

    async def from_cache(self, command, member):
        if self.cache == {}:
            return None

        if member.avatar_url in self.cache[command.name]:
            return copy.deepcopy(self.cache[command.name][member.avatar_url])
        return None

    async def generate_image(self, command, member, manipulation_function, *args, **kwargs):
        cached = await self.from_cache(command, member)

        if cached is None:
            avatar = await self.avatar_bytes(command, member)
            image_bytes = await manipulation_function(avatar, *args, **kwargs)
            await self.add_to_cache(command, image_bytes, member)
        else:
            image_bytes = cached

        return image_bytes

    async def generate_image_embed(self, ctx, member):
        ret = discord.Embed(
            title=f"{ctx.command.name.capitalize()} on {member.display_name}",
            description=f"Requested by {ctx.author.mention}.",
            color=self.bot.color
        )
        ret.set_image(url="attachment://generated.png")

        return ret

    async def generate_cache_structure(self):
        await self.bot.wait_until_ready()
        for command in self.walk_commands():
            if command.cache_images:
                self.cache.update({command.name: {}})

    async def cog_before_invoke(self, ctx):
        await ctx.message.add_reaction("a:anim_discord_loading:514917324709429344")

    async def cog_after_invoke(self, ctx):
        await ctx.message.remove_reaction("a:anim_discord_loading:514917324709429344", ctx.guild.me)

    @commands.command(cls=ImageCommand, cache=True, name="magic")
    async def magic(self, ctx, *, member: discord.Member = None):
        """Content aware scale a member's avatar into another planet."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.magic)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="deepfry", avatar_size=512)
    async def deepfry(self, ctx, *, member: discord.Member = None):
        """Deepfry a member's avatar. It still needs more jpeg."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.deepfry)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="emboss")
    async def emboss(self, ctx, *, member: discord.Member = None):
        """Emboss a member's avatar,"""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.emboss)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="vaporwave", avatar_size=512)
    async def vaporwave(self, ctx, *, member: discord.Member = None):
        """vvvaaapppooorrrwwwaaavvveee"""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.vaporwave)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="floor", avatar_size=128)
    async def floor(self, ctx, *, member: discord.Member = None):
        """The floor is lava and the lava is a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.floor)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="concave")
    async def concave(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a concave lens."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.concave)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="convex")
    async def convex(self, ctx, *, member: discord.Member = None):
        """View a member's avatar through a convex lens."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.convex)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="invert", avatar_size=1024)
    async def invert(self, ctx, *, member: discord.Member = None):
        """Invert a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.invert)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="desat")
    async def desat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Desaturate a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.desat, threshold)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sat")
    async def sat(self, ctx, member: typing.Union[discord.Member] = None, threshold: int = 1):
        """Saturate a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.sat, threshold)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="lsd")
    async def lsd(self, ctx, *, member: discord.Member = None):
        """Take some LSD and look at a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.lsd)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="posterize")
    async def posterize(self, ctx, *, member: discord.Member = None):
        """Posterize a member's avatar,"""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.posterize)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="grayscale", aliases=["greyscale"], avatar_size=512)
    async def grayscale(self, ctx, *, member: discord.Member = None):
        """Grayscale a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.grayscale)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="bend")
    async def bend(self, ctx, *, member: discord.Member = None):
        """Bend a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.bend)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="edge")
    async def edge(self, ctx, *, member: discord.Member = None):
        """Make a member's avatar sharp and edgy."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.edge)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="gay")
    async def gay(self, ctx, *, member: discord.Member = None):
        """Make someone gay. Use at your own discretion."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.gay)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sort")
    async def sort(self, ctx, *, member: discord.Member = None):
        """Sort the pixels of a member's avatar. Makes a pretty gradient most of the time."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.sort)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="sobel")
    async def sobel(self, ctx, *, member: discord.Member = None):
        """Sobel filter a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.sobel)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

        await ctx.send(embed=embed, file=f)

    @commands.command(cls=ImageCommand, cache=True, name="shuffle")
    async def shuffle(self, ctx, *, member: discord.Member = None):
        """Shuffle the pixels in a member's avatar."""
        if member is None:
            member = ctx.author

        img = await self.generate_image(ctx.command, member, imageops.shuffle)
        f = discord.File(img, "generated.png")

        embed = await self.generate_image_embed(ctx, member)

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
