import math


def exp_to_level(exp: int):
    return math.floor(exp ** 0.5 * 0.5) + 1


def coord_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def travel_time(distance: float):
    return distance * 360
