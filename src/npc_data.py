import random

import pygame
from .npc import NPC
from .settings import NPCS_PER_DAY, NPC_IMAGE_FOLDER, NPC_SIZE
from .collisions import rect_collides, clamp_to_world


NPC_NAMES = [
    "Mark", "Anna", "Leo", "Kate", "Nick",
    "Alex", "Mia", "John", "Sara", "Tom",
    "Eva", "Max", "Nina", "Oleg", "Ira",
    "Paul", "Liza", "Dan", "Sofia", "Eric",
    "Mila", "Anton", "Vera", "Roman", "Tina",
]

NPC_POINTS = [
    (540, 378),
    (810, 473),
    (338, 338),
    (1107, 702),
    (1458, 486),
]


def get_safe_npc_point(x, y):
    rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
    clamp_to_world(rect)

    if not rect_collides(rect):
        return rect.x, rect.y

    step = NPC_SIZE

    # ищем ближайшую свободную точку вокруг спавна
    for radius in range(1, 16):
        for offset_x in range(-radius, radius + 1):
            for offset_y in range(-radius, radius + 1):
                if abs(offset_x) != radius and abs(offset_y) != radius:
                    continue

                rect.x = x + offset_x * step
                rect.y = y + offset_y * step
                clamp_to_world(rect)

                if not rect_collides(rect):
                    return rect.x, rect.y

    return x, y


def create_npcs_for_night(night):
    start = (night - 1) * NPCS_PER_DAY
    names = NPC_NAMES[start:start + NPCS_PER_DAY]
    if not names:
        return []

    criminal_name = random.choice(names)
    npcs = []

    for index, name in enumerate(names):
        x, y = NPC_POINTS[index]
        x, y = get_safe_npc_point(x, y)
        is_criminal = name == criminal_name
        image_path = f"{NPC_IMAGE_FOLDER}/npc_{start + index + 1}.png"
        npcs.append(NPC(name, x, y, is_criminal, image_path))

    return npcs
