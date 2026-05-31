import random

from .npc import NPC
from .settings import NPCS_PER_DAY


NPC_NAMES = [
    "Mark", "Anna", "Leo", "Kate", "Nick",
    "Alex", "Mia", "John", "Sara", "Tom",
    "Eva", "Max", "Nina", "Oleg", "Ira",
    "Paul", "Liza", "Dan", "Sofia", "Eric",
    "Mila", "Anton", "Vera", "Roman", "Tina",
]

NPC_POINTS = [
    (400, 280),
    (600, 350),
    (250, 250),
    (820, 520),
    (1080, 360),
]


def create_npcs_for_night(night):
    start = (night - 1) * NPCS_PER_DAY
    names = NPC_NAMES[start:start + NPCS_PER_DAY]
    if not names:
        return []

    criminal_name = random.choice(names)
    npcs = []

    for index, name in enumerate(names):
        x, y = NPC_POINTS[index]
        is_criminal = name == criminal_name
        npcs.append(NPC(name, x, y, is_criminal))

    return npcs
