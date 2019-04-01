from bdo.locations import Coord


class Player:

    def __init__(self, manager, owner):
        self.manager = manager
        self.owner = owner

    @property
    async def name(self):
        record = await self.manager.bot.db.fetch("SELECT name FROM players WHERE ownerid = $1", self.owner.id)
        for value in record[0].values():
            return value

    @property
    async def exp(self):
        record = await self.manager.bot.db.fetch("SELECT name FROM players WHERE ownerid = $1", self.owner.id)
        for value in record[0].values():
            return value

    @property
    async def coord(self):
        records = await self.manager.bot.db.fetch("SELECT l_x, l_y FROM players WHERE ownerid = $1", self.owner.id)
        coords = []
        for record in records:
            for value in record.values():
                coords.append(value)
        return Coord(x, y)

    @property
    async def location(self):
        c = await self.coord
        x, y = c.x, c.y
        for coord, location in self.manager.all_cords.items():
            if coord.x == x and coord.y == y:
                return location
        return None
