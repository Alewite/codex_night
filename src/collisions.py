import pygame

from .settings import MAP_SCALE, WORLD_WIDTH, WORLD_HEIGHT


def make_block_zone(x, y, width, height):
    # перевод координат
    return pygame.Rect(
        int(x * MAP_SCALE),
        int(y * MAP_SCALE),
        int(width * MAP_SCALE),
        int(height * MAP_SCALE),
    )

 # вся коллизия
BLOCK_ZONES = [
    make_block_zone(0, 0, 250, 1700),
    make_block_zone(360, 135, 175, 220),
    make_block_zone(565, 45, 130, 240),
    make_block_zone(745, 55, 150, 240),
    make_block_zone(900, 70, 100, 190),
    make_block_zone(385, 0, 300, 50),
    make_block_zone(775, 0, 200, 50),
    make_block_zone(1165, 0, 125, 130),
    make_block_zone(1290, 0, 60, 100),
    make_block_zone(1410, 0, 140, 325),
    make_block_zone(1145, 177, 135, 165),
    make_block_zone(1280, 275, 140, 50),
    make_block_zone(1170, 440, 280, 180),
    make_block_zone(1175, 760, 290, 280),
    make_block_zone(420, 405, 110, 135),
    make_block_zone(535, 725, 380, 265),
    make_block_zone(915, 725, 90, 200),
    make_block_zone(575, 680, 155, 100),
    make_block_zone(1050, 935, 130, 152),
    make_block_zone(1000, 970, 130, 152),
    make_block_zone(960, 1010, 205, 280),
    make_block_zone(740, 1070, 205, 280),
    make_block_zone(0, 1070, 390, 280),
    
]


def rect_collides(rect):
    # проверка пересечений с каждой зоной коллизии
    for block_zone in BLOCK_ZONES:
        if rect.colliderect(block_zone):
            return True

    return False


def clamp_to_world(rect):
    # ограничение с границами мира
    if rect.left < 0:
        rect.left = 0
    if rect.right > WORLD_WIDTH:
        rect.right = WORLD_WIDTH
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > WORLD_HEIGHT:
        rect.bottom = WORLD_HEIGHT


def move_with_collisions(rect, dx, dy, speed):
    blocked = False

    old_x = rect.x
    rect.x += dx * speed
    clamp_to_world(rect)

    if rect_collides(rect):
        rect.x = old_x
        blocked = True

    old_y = rect.y
    rect.y += dy * speed
    clamp_to_world(rect)

    if rect_collides(rect):
        rect.y = old_y
        blocked = True

    return blocked

