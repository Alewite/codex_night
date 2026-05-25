import pygame

from .settings import INTERACTION_DISTANCE, EVIDENCE_SIZE, EVIDENCE_COLOR


class House:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def is_near_player(self, player):
        # расширяем зону дома для взаимодействия
        zone = self.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)
        return zone.colliderect(player.rect)

    def draw_debug(self, screen, camera_x, camera_y):
        # рисуем дом с учетом камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)


class Boat:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def is_near_player(self, player):
        # расширяем зону яхты для взаимодействия
        zone = self.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)
        return zone.colliderect(player.rect)

    def draw_debug(self, screen, camera_x, camera_y):
        # рисуем яхту с учетом камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, (0, 180, 255), draw_rect, 2)


class Evidence:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, EVIDENCE_SIZE, EVIDENCE_SIZE)
        self.rect.center = (x, y)

    def is_near_player(self, player):
        # расширяем зону улики для подбора
        zone = self.rect.inflate(INTERACTION_DISTANCE, INTERACTION_DISTANCE)
        return zone.colliderect(player.rect)

    def draw(self, screen, camera_x, camera_y):
        # рисуем улику с учетом камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, EVIDENCE_COLOR, draw_rect)
