from bdo.utils.math import coord_distance, travel_time


class Coord:
    """
    A coordinate in/for a Map, Location, or Player.
    This is used for beautifying code and calculation.
    """

    def __init__(self, manager,  x, y):
        self.manager = manager
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"<bdo.locations.Coord x={self.x} y=self.y>"

    def distance_to(self, coord):
        return coord_distance(self.x, self.y, coord.x, coord.y)

    def time_to(self, coord):
        return travel_time(self.distance_to(coord))

    @property
    def location(self):
        for coord, location in self.manager.all_coords.items():
            if coord.x == self.x and coord.y == self.y:
                return location
        return None


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
            self.coords.append(Coord(self.manager, coord[0], coord[1]))

        self.size = len(self.coords)
        self.monsters = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<bdo.locations.Location name={self.name} id={self.id}>"
