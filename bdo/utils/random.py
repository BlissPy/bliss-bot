import numpy as np


def choose_monster(monsters: list):
  p = [monster.rarity for monster in monsters]
  return np.random.choice(monsters, p=p)
