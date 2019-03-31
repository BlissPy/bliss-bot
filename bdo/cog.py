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

        self.players = {}  # set(Player)
        self.bot.loop.create_task(self.import_players())

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
                self.players.add(ply)
            except discord.NotFound:
                pass

    async def create_player(self, ownerid: int, name: str, exp: int = 0, x: int = 8, y: int = 3):
        await self.bot.db.execute(
            "INSERT INTO players VALUES ($1, $2, $3, $4, $5)",
            ownerid, name, exp, x, y,
        )
        player = Player(self, ownerid)
        self.players.add(player)
        return player


class BDOCog(commands.Cog, name="Bliss Desert Online"):

    def __init__(self, bot):
        self.bot = bot
        self.map = Map(bot)

    @commands.command()
    async def create(self, ctx, *, name: str):
        if len(name) > 16:
            return await ctx.send("That name is too long.")

        await self.map.create_player(ctx.author.id, name)

        await ctx.send(f"Welcome to Bliss Desert Online, {name}!")


def setup(bot):
    bot.add_cog(BDOCog(bot))
