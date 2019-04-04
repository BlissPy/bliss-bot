from bdo.locations import Coord
from bdo.utils.math import exp_to_level


class EXP:

    def __init__(self, player, exp):
        self.player = player
        self.points = exp

    @property
    def level(self):
        return exp_to_level(self.points) + 1

    async def set(self, exp: int):
        old_level = exp_to_level(self.points)

        await self.player.manager.bot.db.execute("UPDATE players SET exp = $1 WHERE ownerid = $2", exp, self.player.owner_id)
        self.points = exp

        if old_level < self.level:
            self.player.manager.level_up_queue.append(self.player.owner_id)
        elif old_level > self.level:
            self.player.manager.level_down_queue.append(self.player.owner_id)
        return self.points

    async def add(self, exp: int):
        return await self.set(self.points + exp)

    async def remove(self, exp: int):
        return await self.set(self.points - exp)


class Player:

    def __init__(self, manager, owner_id: int, name: str, x, y, exp):
        self.manager = manager
        self.owner_id = owner_id

        self.name = name
        self.exp = EXP(self, exp)
        self.coord = Coord(self.manager, x, y)

    async def move(self, x, y):
        await self.manager.bot.db.execute("UPDATE players SET l_x = $1, l_y = $2 WHERE ownerid = $3", x, y, self.owner_id)
        self.coord = Coord(self.manager, x, y)
        return self.coord

    async def rename(self, name):
        await self.manager.bot.db.execute("UPDATE players SET name = $1 WHERE ownerid = $2", name, self.owner_id)

    @property
    def location(self):
        return self.coord.location
