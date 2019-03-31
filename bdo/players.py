from bdo.locations import Coord


class Player:

    def __init__(self, manager, owner_id):
        self.manager = manager
        self.owner_id = owner_id

    @property
    async def name(self):
        return await self.manager.bot.db.fetch("SELECT name FROM players WHERE ownerid = $1", self.owner_id)

    @property
    async def exp(self):
        return await self.manager.bot.db.fetch("SELECT name FROM players WHERE exp = $1", self.owner_id)

    @property
    async def coord(self):
        x, y = await self.manager.bot.db.fetch("SELECT l_x, l_y FROM players WHERE exp = $1", self.owner_id)
        return Coord(x, y)

    @property
    async def location(self):
        c = await self.coord
        x, y = c.x, c.y
        for coord, location in self.manager.all_cords.items():
            if coord.x == x and coord.y == y:
                return location
        return None
