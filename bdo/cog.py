import ujson
import discord
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
        for record in await self.bot.db.fetch("SELECT ownerid FROM players;"):
            owner_id = record["ownerid"]
            ply = Player(self, owner_id)
            self.players.update({owner_id: ply})

    async def create_player(self, owner_id: int, name: str, exp: int = 0, x: int = 8, y: int = 3):
        await self.bot.db.execute(
            "INSERT INTO players VALUES ($1, $2, $3, $4, $5)",
            owner_id, name, exp, x, y,
        )
        ply = Player(self, owner_id)
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
            ply = self.map.get_player(message.author.id)
            level = await ply.exp.level
            await message.channel.send(f"{message.author.display_name}, {ply.name} has leveled up to {level}!")

    @commands.command()
    @lack_player()
    async def create(self, ctx, *, name: str):
        if len(name) > 16:
            return await ctx.send("That name is too long.")

        await self.map.create_player(ctx.author.id, name)

        await ctx.send(f"Welcome to Bliss Desert Online, {name}!")

    @commands.command()
    @require_player()
    async def status(self, ctx):
        player = self.map.get_player(ctx.author.id)

        embed = discord.Embed(
            title=await player.name + "'s status",
            color=self.bot.color
        )
        embed.add_field(name="Location", value=(await player.location).name)
        embed.add_field(name="Coord Location", value=await player.coord)
        embed.add_field(name="EXP", value="{} EXP Points".format(await player.exp))

        await ctx.send(embed=embed)

    @commands.command()
    @require_player()
    async def location(self, ctx, location_name: str = None):
        if location_name is None:
            player = self.map.get_player(ctx.author.id)
            location = await player.location
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
    async def fight(self, ctx):
        player = self.map.get_player(ctx.author.id)
        location = await player.location
        monster = choose_monster(location.monsters)
        won = win(player, monster)
        if won:
            exp = monster.exp
            await player.exp.add(exp)
            status = "won"
        else:
            exp = 0
            status = "lost"
        await ctx.send(f"You fought a **{monster.name}** and **{status}**! (+{exp} EXP)")


def setup(bot):
    bot.add_cog(BDOCog(bot))
