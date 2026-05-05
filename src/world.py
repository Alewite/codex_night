import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRASS, ROAD, HOUSE_COLOR, WATER
class World:
    def __init__(self):
        self.house_rect = pygame.Rect(60, 500, 120, 100)
        self.water_rect = pygame.Rect(0, 620, SCREEN_WIDTH, 80)
        self.road_rect = pygame.Rect(0, 300, SCREEN_WIDTH, 90)

    def draw(self, screen):
        screen.fill(GRASS)

        pygame.draw.rect(screen, ROAD, self.road_rect)
        pygame.draw.rect(screen, HOUSE_COLOR, self.house_rect)
        pygame.draw.rect(screen, WATER, self.water_rect)