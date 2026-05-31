import time

import pygame
from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WHITE,
    YELLOW,
    GREEN,
    RED,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    MAX_NIGHTS,
    SUSPICION_TIME,
    EVIDENCE_SUSPICION_TIME,
)
from .player import Player
from .world import World
from .ui import ScannerUI
from .daynight import DayNightManager
from .objects import House, Boat, Evidence
from .npc_data import create_npcs_for_night
from .suspicion import Suspicion
from .story import StoryScreen, INTRO_TEXT, OUTRO_TEXT
from .day_screen import DayScreen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("кодекс ночи")

        self.clock = pygame.time.Clock()
        self.running = True
        self.world = World()
        self.player = Player(100, 100)
        self.font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 46)
        self.big_font = pygame.font.SysFont("arial", 64)

        self.scanner_ui = ScannerUI()
        self.daynight = DayNightManager()
        self.house = House(420, 460, 120, 100)
        self.boat = Boat(270, 970, 120, 60)
        self.npcs = []
        self.evidences = []
        self.carried_evidence = 0
        self.delivered_evidence = 0
        self.criminals_done = 0
        self.suspicion = Suspicion()
        self.game_over = False
        self.game_finished = False
        self.message = ""
        self.last_time = time.monotonic()
        self.day_screen = DayScreen()
        self.intro_active = True
        self.intro_screen = StoryScreen("кодекс ночи", INTRO_TEXT, "SPACE - начать игру")
        self.outro_active = False
        self.outro_screen = StoryScreen("кодекс ночи", OUTRO_TEXT, "SPACE - начать заново")
        self.spawn_npcs()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def get_camera(self):
        # держим игрока около центра экрана
        camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2

        # не выпускаем камеру за края большой карты
        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
        return camera_x, camera_y

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.intro_active:
                    if event.key == pygame.K_SPACE:
                        self.close_intro()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    continue

                if self.outro_active:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    continue

                # проверяем нажатие клавиши e
                if event.key == pygame.K_e:
                    self.handle_action()

                # проверяем нажатие клавиши f
                if event.key == pygame.K_f:
                    if self.daynight.is_night():
                        self.eliminate_near_criminal()

                # начинаем игру заново после поражения
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart_game()

                # закрываем карточку или игру
                if event.key == pygame.K_RETURN:
                    if self.scanner_ui.active:
                        self.scanner_ui.close()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def handle_action(self):
        if self.game_over or self.game_finished:
            return

        if self.scanner_ui.active:
            return

        # меняем день и ночь рядом с домом
        if self.house.is_near_player(self.player):
            self.change_phase_near_house()
            return

        # забираем улику рядом с игроком
        if self.collect_near_evidence():
            return

        # сбрасываем все улики рядом с яхтой
        if self.boat.is_near_player(self.player) and self.carried_evidence > 0:
            self.deposit_evidence()
            return

        # днем сканируем ближайшего npc
        if self.daynight.is_day():
            self.scan_near_npc()

    def close_intro(self):
        self.intro_active = False
        self.last_time = time.monotonic()
        self.day_screen.show(self.daynight.night)

    def restart_game(self):
        self.player = Player(100, 100)
        self.scanner_ui.close()
        self.daynight = DayNightManager()
        self.evidences = []
        self.carried_evidence = 0
        self.delivered_evidence = 0
        self.criminals_done = 0
        self.suspicion.reset()
        self.game_over = False
        self.game_finished = False
        self.outro_active = False
        self.message = ""
        self.last_time = time.monotonic()
        self.day_screen.show(self.daynight.night)
        self.spawn_npcs()

    def finish_game(self):
        self.game_finished = True
        self.outro_active = True
        self.outro_screen.restart()
        self.message = ""

    def spawn_npcs(self):
        self.npcs = create_npcs_for_night(self.daynight.night)

    def has_criminal(self):
        for npc in self.npcs:
            if npc.is_criminal:
                return True
        return False

    def change_phase_near_house(self):
        if self.daynight.is_day():
            self.daynight.change_phase()
            self.message = ""
            return

        if self.has_criminal():
            self.message = "сначала устраните преступника"
            return

        if self.evidences or self.carried_evidence > 0:
            self.message = "сначала сбросьте улику"
            return

        if self.daynight.night < MAX_NIGHTS:
            self.daynight.change_phase()
            self.spawn_npcs()
            self.day_screen.show(self.daynight.night)
            self.message = ""

    def eliminate_near_criminal(self):
        if self.game_over or self.game_finished:
            return

        if not self.daynight.is_night():
            return

        for npc in self.npcs[:]:
            if npc.is_near_player(self.player) and npc.is_criminal and npc.is_scanned:
                evidence = Evidence(npc.rect.centerx, npc.rect.centery)
                self.evidences.append(evidence)
                self.npcs.remove(npc)
                self.criminals_done += 1
                self.message = "цель устранена"
                break

    def collect_near_evidence(self):
        for evidence in self.evidences[:]:
            if evidence.is_near_player(self.player):
                self.carried_evidence += 1
                self.evidences.remove(evidence)
                return True

        return False

    def deposit_evidence(self):
        self.delivered_evidence += self.carried_evidence
        self.carried_evidence = 0

        if self.criminals_done >= MAX_NIGHTS:
            self.finish_game()

    def scan_near_npc(self):
        for npc in self.npcs:
            if npc.is_near_player(self.player):
                npc.scan()
                self.scanner_ui.open(npc)
                break

    def update(self):
        now = time.monotonic()
        dt = min(now - self.last_time, 0.1)
        self.last_time = now

        if self.intro_active or self.outro_active:
            return

        if self.day_screen.is_active(self.daynight.is_day()):
            return

        self.daynight.update()

        if self.game_over or self.game_finished:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0

        # читаем движение игрока с клавиш wasd
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        self.player.move(dx, dy)
        for npc in self.npcs:
            npc.update(self.daynight.is_night())

        if self.daynight.is_night():
            npc = self.get_npc_that_sees_player()
            if npc:
                npc.watch_point(self.player.rect.centerx, self.player.rect.centery)
                self.add_suspicion(dt, SUSPICION_TIME)
                return

            npc, evidence = self.get_npc_that_sees_evidence()
            if npc and evidence:
                npc.watch_point(evidence.rect.centerx, evidence.rect.centery)
                self.add_suspicion(dt, EVIDENCE_SUSPICION_TIME)

    def get_npc_that_sees_player(self):
        for npc in self.npcs:
            if npc.can_see_player(self.player):
                return npc
        return None

    def get_npc_that_sees_evidence(self):
        for npc in self.npcs:
            for evidence in self.evidences:
                if npc.can_see_rect(evidence.rect):
                    return npc, evidence
        return None, None

    def add_suspicion(self, dt, time_limit):
        if self.suspicion.add(dt, time_limit):
            self.game_over = True
            self.message = "вас заметили"

    def draw_daynight_info(self):
        text = self.font.render(self.daynight.get_text(), True, YELLOW)
        self.screen.blit(text, (20, 20))

    def draw_night_overlay(self):
        if self.daynight.is_night():
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

    def draw_evidence_info(self):
        text = self.font.render(
            f"Улики: {self.carried_evidence} | Сброшено: {self.delivered_evidence} | Цели: {self.criminals_done}/{MAX_NIGHTS}",
            True,
            WHITE,
        )

        self.screen.blit(text, (20, 45))

    def draw_suspicion_info(self):
        text = self.font.render(f"Подозреваемость: {self.suspicion.percent()}%", True, RED)
        x = SCREEN_WIDTH - text.get_width() - 20
        self.screen.blit(text, (x, 20))

    def draw_message(self):
        if not self.message:
            return

        color = WHITE
        if self.game_finished:
            color = GREEN
        elif self.game_over:
            color = RED

        text = self.font.render(self.message, True, color)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        self.screen.blit(text, (x, 75))

    def draw_hints(self):
        if self.scanner_ui.active:
            return

        if self.game_over:
            self.scanner_ui.draw_hint(self.screen, self.font, "SPACE - начать заново")
            return

        if self.game_finished:
            return

        if self.house.is_near_player(self.player):
            if self.daynight.is_night() and self.has_criminal():
                self.scanner_ui.draw_hint(self.screen, self.font, "сначала устраните преступника")
                return

            self.scanner_ui.draw_hint(self.screen, self.font, "E - войти домой")
            return

        for evidence in self.evidences:
            if evidence.is_near_player(self.player):
                self.scanner_ui.draw_hint(self.screen, self.font, "E - взять улику")
                return

        if self.boat.is_near_player(self.player) and self.carried_evidence > 0:
            self.scanner_ui.draw_hint(self.screen, self.font, "E - сбросить улику")
            return

        for npc in self.npcs:
            if npc.is_near_player(self.player):
                if self.daynight.is_night() and npc.is_criminal and npc.is_scanned:
                    self.scanner_ui.draw_hint(self.screen, self.font, "F - устранить цель")
                elif self.daynight.is_day():
                    self.scanner_ui.draw_hint(self.screen, self.font, "E - сканировать")
                return

    def draw(self):
        if self.intro_active:
            self.intro_screen.draw(self.screen, self.title_font, self.font)
            pygame.display.flip()
            return

        if self.outro_active:
            self.outro_screen.draw(self.screen, self.title_font, self.font)
            pygame.display.flip()
            return

        if self.day_screen.is_active(self.daynight.is_day()):
            self.day_screen.draw(self.screen, self.big_font)
            pygame.display.flip()
            return

        camera_x, camera_y = self.get_camera()

        self.world.draw(
            self.screen,
            camera_x,
            camera_y,
            self.daynight.is_night()
        )
        self.house.draw_debug(self.screen, camera_x, camera_y)
        self.boat.draw_debug(self.screen, camera_x, camera_y)

        if self.daynight.is_night():
            for npc in self.npcs:
                npc.draw_vision(self.screen, camera_x, camera_y)

        for npc in self.npcs:
            npc.draw(self.screen, self.font, camera_x, camera_y)
        for evidence in self.evidences:
            evidence.draw(self.screen, camera_x, camera_y)

        self.player.draw(self.screen, camera_x, camera_y)

        self.draw_daynight_info()
        self.draw_evidence_info()
        self.draw_suspicion_info()
        self.draw_message()
        self.draw_hints()
        self.scanner_ui.draw(self.screen, self.font)

        pygame.display.flip()
