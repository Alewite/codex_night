import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, PANEL_COLOR, PANEL_BORDER


class ScannerUI:
    def __init__(self):
        self.active = False
        self.npc = None

    def open(self, npc):
        self.active = True
        self.npc = npc

    def close(self):
        self.active = False
        self.npc = None

    def draw_hint(self, screen, font, text):
        hint_text = font.render(text, True, WHITE)

        # ставим подсказку по центру нижней части экрана
        x = SCREEN_WIDTH // 2 - hint_text.get_width() // 2
        y = SCREEN_HEIGHT - 50

        screen.blit(hint_text, (x, y))

    def draw(self, screen, font):
        if not self.active or not self.npc:
            return

        # рисуем карточку сканирования поверх мира
        panel_width = 500
        panel_height = 250
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect)
        pygame.draw.rect(screen, PANEL_BORDER, panel_rect, 3)

        status = "Преступник" if self.npc.is_criminal else "Чист"
        status_color = RED if self.npc.is_criminal else GREEN
        name_text = font.render(f"Имя: {self.npc.name}", True, WHITE)
        status_text = font.render(f"Статус: {status}", True, status_color)
        info_text = font.render("Информация получена после сканирования.", True, WHITE)
        close_text = font.render("ESC - закрыть", True, WHITE)
        screen.blit(name_text, (panel_x + 30, panel_y + 40))
        screen.blit(status_text, (panel_x + 30, panel_y + 90))
        screen.blit(info_text, (panel_x + 30, panel_y + 140))
        screen.blit(close_text, (panel_x + 30, panel_y + 190))
