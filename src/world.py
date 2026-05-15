import pygame

from .settings import WORLD_WIDTH, WORLD_HEIGHT, DAY_MAP_PATH, NIGHT_MAP_PATH
class World:
    def __init__(self):
        self.day_map = pygame.image.load(DAY_MAP_PATH).convert()
        self.night_map = pygame.image.load(NIGHT_MAP_PATH).convert()
        # масштабируем карты до размеров мира
        self.day_map = pygame.transform.scale(self.day_map, (WORLD_WIDTH, WORLD_HEIGHT))
        self.night_map = pygame.transform.scale(self.night_map, (WORLD_WIDTH, WORLD_HEIGHT))

    def draw(self, screen, camera_x, camera_y, is_night):
        if is_night:
            screen.blit(self.night_map, (-camera_x, -camera_y))
        else:
            screen.blit(self.day_map, (-camera_x, -camera_y))