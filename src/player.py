import pygame

from .settings import PLAYER_SIZE, PLAYER_SPEED, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx * PLAYER_SPEED
        self.rect.y += dy * PLAYER_SPEED
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)