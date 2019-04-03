import numpy as np

from bdo.players import Player
from bdo.monsters import Monster


def choose_monster(monsters: list):
    p = [monster.rarity for monster in monsters]
    sum(p)
    p = [1 / r for r in p]
    return np.random.choice(monsters, p=p)


def win(player: Player, monster: Monster):
    level = player.exp.level

    if level in monster.recommended_levels:
        loss_chance = 0.075
    elif level < min(monster.recommended_levels):
        loss_chance = 0.970
    else:
        loss_chance = 0

    win_chance = 1 - loss_chance
    p = [loss_chance, win_chance]
    return np.random.choice([False, True], p=p)
