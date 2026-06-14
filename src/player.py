import pygame

from .settings import PLAYER_SIZE, PLAYER_SPEED, GREEN, PLAYER_IMAGE_PATH
from .collisions import move_with_collisions


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.image = self.load_image()

    def load_image(self):
        try:
            image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        except pygame.error:
            return None

        # сохраняем пропорции спрайта и подгоняем высоту под старый квадрат
        width = int(image.get_width() * (PLAYER_SIZE / image.get_height()))
        return pygame.transform.scale(image, (width, PLAYER_SIZE))

    def move(self, dx, dy):
        # двигаем игрока с проверкой стен и воды
        move_with_collisions(self.rect, dx, dy, PLAYER_SPEED)

    def draw(self, screen, camera_x, camera_y):
        # смещаем игрока относительно камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)
        if self.image:
            # ставим спрайт по центру старого прямоугольника
            image_x = draw_rect.centerx - self.image.get_width() // 2
            image_y = draw_rect.bottom - self.image.get_height()
            screen.blit(self.image, (image_x, image_y))
        else:
            pygame.draw.rect(screen, GREEN, draw_rect)
