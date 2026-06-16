import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, PANEL_BORDER


class MenuScreen:
    def __init__(self):
        button_width = 260
        button_height = 58
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        self.play_rect = pygame.Rect(button_x, 330, button_width, button_height)
        self.exit_rect = pygame.Rect(button_x, 410, button_width, button_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "play"
            if event.key == pygame.K_ESCAPE:
                return "exit"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_rect.collidepoint(event.pos):
                return "play"
            if self.exit_rect.collidepoint(event.pos):
                return "exit"

        return None

    def draw_button(self, screen, font, rect, text):
        # рисуем кнопку меню
        pygame.draw.rect(screen, BLACK, rect)
        pygame.draw.rect(screen, PANEL_BORDER, rect, 2)
        label = font.render(text, True, WHITE)
        x = rect.centerx - label.get_width() // 2
        y = rect.centery - label.get_height() // 2
        screen.blit(label, (x, y))

    def draw(self, screen, title_font, font):
        screen.fill(BLACK)

        title = title_font.render("кодекс ночи", True, WHITE)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title, (title_x, 210))

        self.draw_button(screen, font, self.play_rect, "Играть")
        self.draw_button(screen, font, self.exit_rect, "Выйти")
