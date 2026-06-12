import random
import math

import pygame
from .settings import (
    NPC_SIZE,
    NPC_COLOR,
    BLACK,
    GREEN,
    RED,
    INTERACTION_DISTANCE,
    NPC_SPEED,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    VISION_LENGTH,
    VISION_WIDTH,
    VISION_COLOR,
)


class NPC:
    def __init__(self, name, x, y, is_criminal=False, image_path=None):
        self.name = name
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.is_criminal = is_criminal
        self.is_scanned = False
        self.image = self.load_image(image_path)
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])
        self.look_dx = 0
        self.look_dy = 1
        self.move_timer = 0
        self.is_watching = False

    def load_image(self, image_path):
        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            return None

        # сохраняем пропорции спрайта и подгоняем высоту под старый квадрат
        width = int(image.get_width() * (NPC_SIZE / image.get_height()))
        return pygame.transform.scale(image, (width, NPC_SIZE))

    def update(self, is_night=False):
        if self.is_watching:
            return

        self.move_timer += 1
        if self.move_timer >= 60:
            # случайно выбираем направление движения npc
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.move_timer = 0

        if self.dx != 0 or self.dy != 0:
            self.look_dx = self.dx
            self.look_dy = self.dy

        speed = NPC_SPEED
        if is_night:
            speed = max(1, NPC_SPEED // 2)

        # двигаем npc в выбранном направлении
        self.rect.x += self.dx * speed
        self.rect.y += self.dy * speed

        # не выпускаем npc за границы мира
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WORLD_HEIGHT:
            self.rect.bottom = WORLD_HEIGHT

    def scan(self):
        self.is_scanned = True

    def is_near_player(self, player):
        distance = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        return distance < INTERACTION_DISTANCE

    def get_name_color(self):
        if not self.is_scanned:
            return BLACK
        elif self.is_criminal:
            return RED
        return GREEN

    def get_look_vector(self):
        length = math.hypot(self.look_dx, self.look_dy)
        if length == 0:
            return 0, 1
        return self.look_dx / length, self.look_dy / length

    def can_see_player(self, player):
        return self.can_see_rect(player.rect)

    def can_see_rect(self, rect):
        look_x, look_y = self.get_look_vector()
        target_x = rect.centerx - self.rect.centerx
        target_y = rect.centery - self.rect.centery
        forward_distance = target_x * look_x + target_y * look_y

        if forward_distance < 0 or forward_distance > VISION_LENGTH:
            return False

        side_distance = abs(target_x * -look_y + target_y * look_x)
        cone_width = (forward_distance / VISION_LENGTH) * (VISION_WIDTH / 2)
        return side_distance <= cone_width

    def watch_point(self, x, y):
        self.is_watching = True
        self.dx = 0
        self.dy = 0
        self.look_dx = x - self.rect.centerx
        self.look_dy = y - self.rect.centery

    def draw_vision(self, screen, camera_x, camera_y):
        look_x, look_y = self.get_look_vector()
        side_x = -look_y
        side_y = look_x
        start_x = self.rect.centerx - camera_x
        start_y = self.rect.centery - camera_y
        end_x = start_x + look_x * VISION_LENGTH
        end_y = start_y + look_y * VISION_LENGTH

        points = [
            (start_x, start_y),
            (end_x + side_x * VISION_WIDTH / 2, end_y + side_y * VISION_WIDTH / 2),
            (end_x - side_x * VISION_WIDTH / 2, end_y - side_y * VISION_WIDTH / 2),
        ]

        # рисуем конус зрения поверх карты
        vision_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(vision_surface, VISION_COLOR, points)
        screen.blit(vision_surface, (0, 0))

    def draw(self, screen, font, camera_x, camera_y):
        draw_rect = self.rect.move(-camera_x, -camera_y)

        if self.image:
            # ставим спрайт по центру старого прямоугольника
            image_x = draw_rect.centerx - self.image.get_width() // 2
            image_y = draw_rect.bottom - self.image.get_height()
            screen.blit(self.image, (image_x, image_y))
        else:
            pygame.draw.rect(screen, NPC_COLOR, draw_rect)
        name_color = self.get_name_color()
        name_text = font.render(self.name, True, name_color)
        text_x = draw_rect.centerx - name_text.get_width() // 2
        text_y = draw_rect.y - 22
        screen.blit(name_text, (text_x, text_y))
