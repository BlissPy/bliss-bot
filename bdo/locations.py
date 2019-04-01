import math


class Coord:
    """
    A coordinate in/for a Map, Location, or Player.
    This is used for beautifying code and calculation.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def distance_to(self, coord):
        x1, y1 = self.x, self.y
        x2, y2 = coord.x, coord.y

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class Location:
    """
    Represents a location in the Bliss Desert Online RPG.
    Locations make up the map.
    """

    def __init__(self, manager, **data):
        self.manager = manager

        self.id = data.get("id")
        self.name = data.get("name")
        self.description = data.get("description")
        self.recommended = {
            "ap": data.get("ap"),
            "dp": data.get("ap")
        }

        self.coords = []
        coord_data = data.get("coords")
        for coord in coord_data:
            self.coords.append(Coord(coord[0], coord[1]))

        self.size = len(self.coords)
