import pygame

from .settings import PLAYER_SIZE, PLAYER_SPEED, GREEN, WORLD_WIDTH, WORLD_HEIGHT


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        # двигаем игрока по осям x и y
        self.rect.x += dx * PLAYER_SPEED
        self.rect.y += dy * PLAYER_SPEED

        # не выпускаем игрока за границы мира
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WORLD_HEIGHT:
            self.rect.bottom = WORLD_HEIGHT

    def draw(self, screen, camera_x, camera_y):
        # смещаем игрока относительно камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, GREEN, draw_rect)
