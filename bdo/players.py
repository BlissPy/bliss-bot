from bdo.locations import Coord
from bdo.utils.math import exp_to_level


class EXP:

    def __init__(self, player):
        self.player = player

    @property
    async def level(self):
        return exp_to_level(await self.points)

    @property
    async def points(self):
        record = await self.player.manager.bot.db.fetch("SELECT exp FROM players WHERE ownerid = $1", self.player.owner_id)
        return record[0]['exp']

    async def add(self, exp: int):
        current = await self.points
        old_level = exp_to_level(current)
        await self.player.manager.bot.db.execute("UPDATE players SET exp = $1 WHERE ownerid = $2", current + exp, self.player.owner_id)
        if old_level < exp_to_level(current + exp):
            self.player.manager.level_up_queue.append(self.player.owner_id)


class Player:

    def __init__(self, manager, owner_id: int):
        self.manager = manager
        self.owner_id = owner_id
        self.exp = EXP(self)

    @property
    async def name(self):
        record = await self.manager.bot.db.fetch("SELECT name FROM players WHERE ownerid = $1", self.owner_id)
        return record[0]['name']

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

    async def move(self, x, y):
        await self.manager.bot.db.execute("UPDATE players SET l_x = $1, l_y = $2 WHERE ownerid = $3", x, y, self.owner_id)
        return await self.coord
