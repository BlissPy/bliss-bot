import datetime
import random
import typing

import ujson
import discord
import humanize
from discord.ext import commands

from bdo.locations import Location
from bdo.players import Player
from bdo.monsters import Monster
from bdo.utils.checks import lack_player, require_player
from bdo.utils.random import choose_monster, win


class Map:
    """
    Essentially the manager for all the Locations and Players.
    """

    def __init__(self, bot):
        self.bot = bot

        with open("bdo_config.json", "r") as f:
            self.config = ujson.load(f)

        self.locations = {}  # dict(id: Location)
        self.all_coords = {}  # dict(Coord: Location)
        self.import_locations()

        self.monsters = {}  # dict(id: Monster)
        self.import_monsters()

        self.players = {}  # dict(owner_id: Player)
        self.bot.loop.create_task(self.import_players())

        self.level_up_queue = []
        self.level_down_queue = []

    def get_player(self, owner_id):
        return self.players[owner_id]

    def get_location(self, text: str):
        try:
            return self.locations[int(text)]
        except ValueError:
            return discord.utils.find(
                lambda location: location.name.lower() == text.lower(),
                list(self.locations.values())
            )
        except KeyError:
            return None

    def import_locations(self):
        for data in self.config["locations"]:
            loc = Location(self, **data)
            self.locations.update({loc.id: loc})
            for coord in loc.coords:
                self.all_coords.update({coord: loc})

    def import_monsters(self):
        for data in self.config["monsters"]:
            monster = Monster(self, **data)
            for location in monster.spawn_locations:
                location.monsters.append(monster)
            self.monsters.update({monster.id: monster})

    async def import_players(self):
        for record in await self.bot.db.fetch("SELECT * FROM players;"):
            ply = Player(self, record["ownerid"], record["name"], record["l_x"], record["l_y"], record["exp"])
            self.players.update({record["ownerid"]: ply})

    async def create_player(self, owner_id: int, name: str, exp: int = 0, x: int = 8, y: int = 3):
        await self.bot.db.execute(
            "INSERT INTO players VALUES ($1, $2, $3, $4, $5)",
            owner_id, name, exp, x, y,
        )
        ply = Player(self, owner_id, name, x, y, exp)
        self.players.update({owner_id: ply})
        return ply


class BDOCog(commands.Cog, name="Bliss Desert Online"):

    def __init__(self, bot):
        self.bot = bot
        self.map = None
        self.bot.loop.create_task(self.create_map())

    async def create_map(self):
        await self.bot.wait_until_ready()
        self.map = Map(self.bot)
        self.bot.map = self.map

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.map is None:
            return

        if message.author.id in self.map.level_up_queue:
            self.map.level_up_queue.remove(message.author.id)
            ply = self.map.get_player(message.author.id)
            await message.channel.send(f"{message.author.display_name}, {ply.name} has leveled up to {ply.exp.level}! Keep going.")
        elif message.author.id in self.map.level_down_queue:
            self.map.level_down_queue.remove(message.author.id)
            ply = self.map.get_player(message.author.id)
            await message.channel.send(f"{message.author.display_name}, {ply.name} has leveled down to {ply.exp.level}. Yikes.")

    @commands.command()
    @require_player()
    @commands.is_owner()
    async def tp(self, ctx, owner: typing.Optional[discord.User] = None, x: int = 1, y: int = 1):
        if owner is None:
            owner = ctx.author
        player = self.map.get_player(owner.id)
        old = player.coord
        new = await player.move(x, y)
        await ctx.send(f"Moved {player.name} {round(old.distance_to(new), 2)}u from {old} to {new}.")

    @commands.command()
    @lack_player()
    async def create(self, ctx, *, name: str):
        if len(name) > 16:
            return await ctx.send("That name is too long.")

        await self.map.create_player(ctx.author.id, name)

        await ctx.send(f"Welcome to Bliss Desert Online, {name}!")

    @commands.command(aliases=["profile"])
    @require_player()
    async def status(self, ctx):
        player = self.map.get_player(ctx.author.id)

        embed = discord.Embed(
            title=f"{player.name}'s status",
            color=self.bot.color
        )
        embed.add_field(name="Location", value=player.location.name)
        embed.add_field(name="Coord Location", value=player.coord)
        embed.add_field(name="EXP", value=f"{player.exp.points} EXP Points")
        embed.add_field(name="Level", value=player.exp.level)
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @require_player()
    async def location(self, ctx, location_name: str = None):
        if location_name is None:
            player = self.map.get_player(ctx.author.id)
            location = player.location
        else:
            location = self.map.get_location(location_name)
            if location is None:
                return await ctx.send("No location with that name or id exists. Please try again.")

        embed = discord.Embed(
            title=location.name,
            description=location.description,
            color=self.bot.color
        )
        embed.add_field(name="Recommended AP", value=f"AP: {location.recommended['ap']}, DP: {location.recommended['dp']}")
        embed.add_field(name="Size", value=location.size)
        embed.add_field(
            name="Owned Coords",
            value=", ".join(str(coord) for coord in location.coords)
        )

        await ctx.send(embed=embed)

    @commands.command()
    @require_player()
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def fight(self, ctx):
        player = self.map.get_player(ctx.author.id)
        location = player.location
        monster = choose_monster(location.monsters)
        won = win(player, monster)
        if won:
            exp = monster.exp
            player.exp.add(exp)
            status = "won"
        else:
            exp = 0
            status = "lost"
        await ctx.send(f"You fought a **{monster.name}** and **{status}**! (+{exp} EXP)")

    @commands.group(aliases=["level"])
    @require_player()
    async def exp(self, ctx, owner: discord.User = None):
        if ctx.invoked_subcommand is None:
            if owner is None:
                owner = ctx.author
            player = self.map.get_player(owner.id)
            await ctx.send(f"{player.name}, you have **{player.exp.points} EXP points** which makes you **level {player.exp.level}**.")

    @exp.command()
    @require_player()
    @commands.is_owner()
    async def exp_set(self, ctx, owner: typing.Optional[discord.User] = None, new_exp: int = 0):
        if owner is None:
            owner = ctx.author
        player = self.map.get_player(owner.id)
        old_exp = player.exp.points
        old_level = player.exp.level

        new_exp = player.exp.set(new_exp)

        await ctx.send(f"{player.name}'s EXP has been changed from {old_exp} (lvl {old_level}) to {new_exp} ({player.exp.level}).")

    @commands.command()
    @require_player()
    @commands.is_owner()
    async def walk(self, ctx, location: typing.Optional[str] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None):
        if location is None and x is None:
            return await ctx.send("This command allows you to go to a specific coordinate or a general location. Here are some examples of it's use.\n"
                                    "`bl walk 8 3` to walk to the coords (8, 3)\n"
                                    "`bl walk velia` to walk to Velia by it's name.\n"
                                    "`bl walk 1` to walk to Velia by it's location ID.")
        elif location is None and not x is None and y is None:
            location = self.map.get_location(x)
            coord = random.choice(location.coords)
        elif location is not None:
            location = self.map.get_location(location)
            coord = random.choice(location.coords)
        elif x is not None and y is not None:
            coord = Coord(self.map, x, y)
            location = coord.location

        player = self.map.get_player(ctx.author.id)

        await ctx.send(
            "This action is not ready for use yet. Sending stats."
            f"Traveling from {player.location} ({player.coord}) to {location} ({player.coord}),"
            f"a distance of {player.coord.distance_to(coord)}u, will take {humanize.naturaltime(datetime.timedelta(seconds=player.coord.time_to(coord)))}."
        )



def setup(bot):
    bot.add_cog(BDOCog(bot))
