from bdo.locations import Coord


class Player:

    def __init__(self, manager, owner_id: int):
        self.manager = manager
        self.owner_id = owner_id

    @property
    async def name(self):
        record = await self.manager.bot.db.fetch("SELECT name FROM players WHERE ownerid = $1", self.owner_id)
        return record[0]['name']

    @property
    async def exp(self):
        record = await self.manager.bot.db.fetch("SELECT exp FROM players WHERE ownerid = $1", self.owner_id)
        return record[0]['exp']

    @property
    async def coord(self):
        record = await self.manager.bot.db.fetch("SELECT l_x, l_y FROM players WHERE ownerid = $1", self.owner_id)
        record = record[0]
        return Coord(record["l_x"], record["l_y"])

    @property
    async def location(self):
        c = await self.coord
        x, y = c.x, c.y
        for coord, location in self.manager.all_coords.items():
            if coord.x == x and coord.y == y:
                return location
        return None

    async def to_dict(self):
        return {
            "name": await self.name,
            "exp": await self.exp,
            "coord": await self.coord,
            "location": await self.location
        }
