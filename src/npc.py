import pygame, random
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
)
class NPC:
    def __init__(self, name,x, y, is_criminal=False):
        self.name = name
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.is_criminal = is_criminal
        self.is_scanned = False
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])
        self.move_timer = 0
    def update(self):
        self.move_timer += 1
        if self.move_timer >= 60:
            # Случайно выбираем направление движения NPC по X и Y
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.move_timer = 0
        # движение NPC в выбранном направлении с заданной скоростью
        self.rect.x += self.dx * NPC_SPEED
        self.rect.y += self.dy * NPC_SPEED

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
    def draw(self, screen, font, camera_x, camera_y):
        draw_rect = self.rect.move(-camera_x, -camera_y)

        pygame.draw.rect(screen, NPC_COLOR, draw_rect)
        name_color = self.get_name_color()
        name_text = font.render(self.name, True, name_color)
        text_x = draw_rect.centerx - name_text.get_width() // 2
        text_y = draw_rect.y - 22
        screen.blit(name_text, (text_x, text_y))