import random
import math

import pygame
from .settings import (
    NPC_SIZE,
    NPCS_PER_DAY,
    NPC_IMAGE_FOLDER,
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
from .collisions import move_with_collisions, rect_collides, clamp_to_world


NPC_NAMES = [
    "Mark", "Anna", "Leo", "Kate", "Nick",
    "Alex", "Mia", "John", "Sara", "Tom",
    "Eva", "Max", "Nina", "Oleg", "Ira",
    "Paul", "Liza", "Dan", "Sofia", "Eric",
    "Mila", "Anton", "Vera", "Roman", "Tina",
]


class NPC:
    def __init__(self, name, x, y, is_criminal=False, image_path=None):
        # основные данные нпс
        self.name = name
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.is_criminal = is_criminal
        self.is_scanned = False
        self.image = self.load_image(image_path)

        # движение
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

        # взгяд
        self.look_dx = 0
        self.look_dy = 1
        self.move_timer = 0

    def load_image(self, image_path):
        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # если спрайт не найден, нпс - квадратик
            return None

        width = int(image.get_width() * (NPC_SIZE / image.get_height()))
        return pygame.transform.scale(image, (width, NPC_SIZE))

    def update(self, is_night=False):
        # изменение направления движения
        self.move_timer += 1
        if self.move_timer >= 60:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.move_timer = 0

        if self.dx != 0 or self.dy != 0:
            self.look_dx = self.dx
            self.look_dy = self.dy

        if is_night and self.move_timer % 2 == 1:
            return
        
        blocked = move_with_collisions(self.rect, self.dx, self.dy, NPC_SPEED)
        if blocked:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])

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
        # проверка игрока через общий метод видимости
        return self.can_see_rect(player.rect)

    def can_see_rect(self, rect):
        look_x, look_y = self.get_look_vector()

        # вектор от нпс до цели
        target_x = rect.centerx - self.rect.centerx
        target_y = rect.centery - self.rect.centery

        # расстояние вперед по направлению взгляда
        forward_distance = target_x * look_x + target_y * look_y

        if forward_distance < 0 or forward_distance > VISION_LENGTH:
            return False
        side_distance = abs(target_x * -look_y + target_y * look_x)

        cone_width = (forward_distance / VISION_LENGTH) * (VISION_WIDTH / 2)
        return side_distance <= cone_width

    def draw_vision(self, screen, camera_x, camera_y):
        #треугольник конуса зрения
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

        # конус поверх карты
        vision_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(vision_surface, VISION_COLOR, points)
        screen.blit(vision_surface, (0, 0))

    def draw(self, screen, font, camera_x, camera_y):
        # смещение нпс относительно камеры
        draw_rect = self.rect.move(-camera_x, -camera_y)

        if self.image:
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


class NPCFactory:
    def __init__(self, names):
        self.names = names

    def get_names_for_day(self, day):
        start = (day - 1) * NPCS_PER_DAY
        return start, self.names[start:start + NPCS_PER_DAY]

    def get_random_point(self, used_rects):
        rect = pygame.Rect(0, 0, NPC_SIZE, NPC_SIZE)

        min_distance = NPC_SIZE * 2

        # ищем случайную свободную точку на карте
        for _ in range(500):
            rect.x = random.randint(0, WORLD_WIDTH - NPC_SIZE)
            rect.y = random.randint(0, WORLD_HEIGHT - NPC_SIZE)
            clamp_to_world(rect)

            if rect_collides(rect):
                continue

            if self.is_too_close(rect, used_rects, min_distance):
                continue

            return rect.x, rect.y

        return WORLD_WIDTH // 2, WORLD_HEIGHT // 2

    def is_too_close(self, rect, used_rects, min_distance):
        # проверяем что новая точка не слишком близко к уже занятым
        for used_rect in used_rects:
            distance = ((rect.centerx - used_rect.centerx) ** 2 + (rect.centery - used_rect.centery) ** 2) ** 0.5
            if distance < min_distance:
                return True

        return False

    def create_for_day(self, day):
        start, names = self.get_names_for_day(day)
        if not names:
            return []

        # выбор преступника
        criminal_name = random.choice(names)
        npcs = []
        used_rects = []

        for index, name in enumerate(names):
            x, y = self.get_random_point(used_rects)
            is_criminal = name == criminal_name

            image_path = f"{NPC_IMAGE_FOLDER}/npc_{start + index + 1}.png"
            npc = NPC(name, x, y, is_criminal, image_path)
            npcs.append(npc)
            used_rects.append(npc.rect.copy())

        return npcs


def create_npcs_for_day(day):
    return NPCFactory(NPC_NAMES).create_for_day(day)
