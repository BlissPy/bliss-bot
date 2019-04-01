import ujson
import discord
from discord.ext import commands

from bdo.locations import Location
from bdo.players import Player


class Map:
    """
    Essentially the manager for all the Locations and Players.
    """

    def __init__(self, bot):
        self.bot = bot

        self.locations = {}  # dict(id: Location)
        self.all_coords = {}  # dict(Coord: Location)

        with open("bdo_config.json", "r") as f:
            self.config = ujson.load(f)["locations"]

        self.import_locations()

        self.players = {}  # dict(owner_id: Player)
        self.bot.loop.create_task(self.import_players())

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

    def import_locations(self):
        for data in self.config:
            loc = Location(self, **data)
            self.locations.update({loc.id: loc})
            for coord in loc.coords:
                self.all_coords.update({coord: loc})

    async def import_players(self):
        for ownerid in await self.bot.db.fetch("SELECT ownerid FROM players;"):
            try:
                ply = Player(self, self.bot.get_user(ownerid))
                self.players.update({ownerid: ply})
            except discord.NotFound:
                pass

    async def create_player(self, ownerid: int, name: str, exp: int = 0, x: int = 8, y: int = 3):
        await self.bot.db.execute(
            "INSERT INTO players VALUES ($1, $2, $3, $4, $5)",
            ownerid, name, exp, x, y,
        )
        ply = Player(self, ownerid)
        self.players.update({ownerid: ply})
        return ply


class BDOCog(commands.Cog, name="Bliss Desert Online"):

    def __init__(self, bot):
        self.bot = bot
        self.map = None
        self.bot.loop.create_task(self.create_map())

    async def create_map(self):
        await self.bot.wait_until_ready()
        self.map = Map(self.bot)

    def has_player(self):
        def predicate(ctx):
            if ctx.author.id in self.map.players:
                return True
            return False
        return commands.check(predicate)

    @commands.command()
    @has_player()
    async def create(self, ctx, *, name: str):
        if len(name) > 16:
            return await ctx.send("That name is too long.")

        await self.map.create_player(ctx.author.id, name)

        await ctx.send(f"Welcome to Bliss Desert Online, {name}!")

    @commands.command()
    async def location(self, ctx, location_name: str = None):
        if location_name is None:
            player = self.map.get_player()
            location = player.location
        else:
            location = self.map.get_location(location_name)

        embed = discord.Embed(
            title=location.name,
            description=location.description,
            color=self.bot.color
        )
        embed.add_field(name="Recommended AP", value=location.recommended)
        embed.add_field(name="Size", value=location.size)
        embed.add_field(
            name="Owned Coords",
            value=", ".join(str(coord) for coord in location.coords)
        )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(BDOCog(bot))
