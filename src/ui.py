import pygame

from .settings import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, PANEL_COLOR, PANEL_BORDER, MAX_DAYS


class UIScreen:
    def __init__(self):
        self.active = False

    def show(self):
        self.active = True

    def hide(self):
        self.active = False


class DayScreen(UIScreen):
    def __init__(self):
        super().__init__()
        # текст крупной заставки дня
        self.text = ""

    def show(self, day):
        super().show()
        self.text = f"ДЕНЬ {day}"

    def is_active(self, is_day):
        return self.active and is_day

    def draw(self, screen, font):
        screen.fill(BLACK)

        text = font.render(self.text, True, WHITE)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (x, y))


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

    def draw(self, screen, font):
        if not self.active or not self.npc:
            return
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
        close_text = font.render("RETURN - закрыть", True, WHITE)
        screen.blit(name_text, (panel_x + 30, panel_y + 40))
        screen.blit(status_text, (panel_x + 30, panel_y + 90))
        screen.blit(close_text, (panel_x + 30, panel_y + 190))


class GameHUD:
    def draw_daynight_info(self, screen, font, daynight):
        # текущая фаза
        text = font.render(daynight.get_text(), True, WHITE)
        screen.blit(text, (20, 20))

    def draw_evidence_info(self, screen, font, carried_evidence, delivered_evidence, criminals_done):
        text = font.render(
            f"Улики: {carried_evidence} | Сброшено: {delivered_evidence} | Цели: {criminals_done}/{MAX_DAYS}",
            True,
            WHITE,
        )
        screen.blit(text, (20, 45))

    def draw_suspicion_info(self, screen, font, suspicion):
        text = font.render(f"Подозреваемость: {suspicion.percent()}%", True, WHITE)
        x = SCREEN_WIDTH - text.get_width() - 20
        screen.blit(text, (x, 20))

    def draw_message(self, screen, font, message):
        if not message:
            return

        text = font.render(message, True, WHITE)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (x, 75))

    def draw_hint(self, screen, font, text):
        hint_text = font.render(text, True, WHITE)
        x = SCREEN_WIDTH // 2 - hint_text.get_width() // 2
        y = SCREEN_HEIGHT - 50
        screen.blit(hint_text, (x, y))

    def get_hint_text(self, game):
        if game.scanner_ui.active:
            return ""

        if game.game_over:
            return "SPACE - начать заново"

        if game.game_finished:
            return ""

        if game.house.is_near_player(game.player):
            if game.daynight.is_night() and game.interactions.has_criminal():
                return "сначала устраните преступника"

            return "E - войти домой"

        for evidence in game.evidences:
            if evidence.is_near_player(game.player):
                return "E - взять улику"

        if game.boat.is_near_player(game.player) and game.carried_evidence > 0:
            return "E - сбросить улику"

        for npc in game.npcs:
            if npc.is_near_player(game.player):
                if game.daynight.is_night() and npc.is_criminal and npc.is_scanned:
                    return "F - устранить цель"
                elif game.daynight.is_day():
                    return "E - сканировать"

                return ""

        return ""

    def draw_hints(self, screen, font, game):
        hint_text = self.get_hint_text(game)
        if hint_text:
            self.draw_hint(screen, font, hint_text)

    def draw(self, screen, font, game):
        # рисуем весь hud игры
        self.draw_daynight_info(screen, font, game.daynight)
        self.draw_evidence_info(screen, font, game.carried_evidence, game.delivered_evidence, game.criminals_done)
        self.draw_suspicion_info(screen, font, game.suspicion)
        self.draw_message(screen, font, game.message)
        self.draw_hints(screen, font, game)
