import random

import pygame
from .npc import NPC
from .settings import NPCS_PER_DAY, NPC_IMAGE_FOLDER, NPC_SIZE, WORLD_WIDTH, WORLD_HEIGHT
from .collisions import rect_collides, clamp_to_world


NPC_NAMES = [
    "Mark", "Anna", "Leo", "Kate", "Nick",
    "Alex", "Mia", "John", "Sara", "Tom",
    "Eva", "Max", "Nina", "Oleg", "Ira",
    "Paul", "Liza", "Dan", "Sofia", "Eric",
    "Mila", "Anton", "Vera", "Roman", "Tina",
]

def get_random_npc_point(used_rects):
    rect = pygame.Rect(0, 0, NPC_SIZE, NPC_SIZE)
    min_distance = NPC_SIZE * 2

    # ищем случайную свободную точку на карте
    for _ in range(500):
        rect.x = random.randint(0, WORLD_WIDTH - NPC_SIZE)
        rect.y = random.randint(0, WORLD_HEIGHT - NPC_SIZE)
        clamp_to_world(rect)

        if rect_collides(rect):
            continue

        too_close = False
        for used_rect in used_rects:
            distance = ((rect.centerx - used_rect.centerx) ** 2 + (rect.centery - used_rect.centery) ** 2) ** 0.5
            if distance < min_distance:
                too_close = True
                break

        if not too_close:
            return rect.x, rect.y

    return WORLD_WIDTH // 2, WORLD_HEIGHT // 2


def create_npcs_for_night(night):
    start = (night - 1) * NPCS_PER_DAY
    names = NPC_NAMES[start:start + NPCS_PER_DAY]
    if not names:
        return []

    criminal_name = random.choice(names)
    npcs = []
    used_rects = []

    for index, name in enumerate(names):
        x, y = get_random_npc_point(used_rects)
        is_criminal = name == criminal_name
        image_path = f"{NPC_IMAGE_FOLDER}/npc_{start + index + 1}.png"
        npc = NPC(name, x, y, is_criminal, image_path)
        npcs.append(npc)
        used_rects.append(npc.rect.copy())

    return npcs
