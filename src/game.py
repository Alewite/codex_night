import time

import pygame
from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    SUSPICION_TIME,
    EVIDENCE_SUSPICION_TIME,
    DAY_SCREEN_FRAMES,
    INTRO_AUDIO_PATH,
    OUTRO_AUDIO_PATH,
)
from .player import Player
from .world import World
from .ui import ScannerUI, DayScreen, GameHUD
from .daynight import DayNightManager
from .objects import House, Boat
from .npc import NPCFactory, NPC_NAMES
from .suspicion import Suspicion
from .story import StoryScreen, INTRO_TEXT, OUTRO_TEXT
from .menu import MenuScreen
from .audio import AudioManager
from .interactions import InteractionManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("кодекс ночи")

        self.clock = pygame.time.Clock()
        self.running = True
        self.world = World()
        self.player = self.create_player()
        self.font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 46)
        self.big_font = pygame.font.SysFont("arial", 64)

        # ui и игровые менеджеры
        self.scanner_ui = ScannerUI()
        self.hud = GameHUD()
        self.daynight = DayNightManager()
        self.npc_factory = NPCFactory(NPC_NAMES)
        self.interactions = InteractionManager(self)

        self.house = House(675, 800, 50, 20)
        self.boat = Boat(300, 260, 81, 162)

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

        # экран дня и меню
        self.day_screen = DayScreen()
        self.day_screen_frames = 0
        self.menu_active = True
        self.menu_screen = MenuScreen()

        # интро и аутро
        self.intro_active = True
        self.intro_started = False
        self.intro_screen = StoryScreen("кодекс ночи", INTRO_TEXT, "SPACE - начать игру", INTRO_AUDIO_PATH)
        self.outro_active = False
        self.outro_screen = StoryScreen("кодекс ночи", OUTRO_TEXT, "SPACE - начать заново", OUTRO_AUDIO_PATH)

        # менеджер звуков игры
        self.audio = AudioManager()
        self.spawn_npcs()

    def create_player(self):
        return Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

    def run(self):
        # главный цикл игры
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def get_camera(self):        # центрируем камеру на игроке
        camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2

        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
        return camera_x, camera_y

    def handle_events(self):
        # обработка всех событий окна и клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.menu_active:
                self.handle_menu_event(event)
                continue

            if event.type == pygame.KEYDOWN:
                if self.intro_active:
                    if event.key == pygame.K_SPACE:
                        self.close_intro()
                    if event.key == pygame.K_ESCAPE:
                        self.intro_screen.stop_audio()
                        self.running = False
                    continue
                if self.outro_active:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                    if event.key == pygame.K_ESCAPE:
                        self.outro_screen.stop_audio()
                        self.running = False
                    continue

                if event.key == pygame.K_e:
                    self.interactions.handle_action()
                if event.key == pygame.K_f:
                    self.interactions.eliminate_near_criminal()

                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart_game()

                if event.key == pygame.K_RETURN:
                    if self.scanner_ui.active:
                        self.scanner_ui.close()
                if event.key == pygame.K_ESCAPE:
                    self.open_menu()

    def handle_menu_event(self, event):
        action = self.menu_screen.handle_event(event)

        if action == "play":
            self.close_menu()
        elif action == "exit":
            self.audio.stop_phase_sound()
            self.running = False

    def open_menu(self):
        self.menu_active = True
        self.scanner_ui.close()
        self.audio.stop_phase_sound()

    def close_menu(self):
        self.menu_active = False
        self.last_time = time.monotonic()

        if self.intro_active and not self.intro_started:
            self.intro_screen.restart()
            self.intro_started = True
        elif not self.outro_active:
            self.audio.play_phase_sound(self.daynight.is_night())

    def close_intro(self):
        self.intro_screen.stop_audio()
        self.intro_active = False
        self.last_time = time.monotonic()
        self.show_day_screen()
        self.audio.play_phase_sound(self.daynight.is_night())

    def show_day_screen(self):
        self.day_screen.show(self.daynight.day)
        self.day_screen_frames = DAY_SCREEN_FRAMES

    def restart_game(self):
        self.intro_screen.stop_audio()
        self.outro_screen.stop_audio()
        self.audio.stop_phase_sound()
        self.player = self.create_player()
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
        self.show_day_screen()
        self.spawn_npcs()
        self.audio.play_phase_sound(self.daynight.is_night())

    def finish_game(self):
        self.audio.stop_phase_sound()
        self.game_finished = True
        self.outro_active = True
        self.outro_screen.restart()
        self.message = ""

    def spawn_npcs(self):
        self.npcs = self.npc_factory.create_for_day(self.daynight.day)

    def update(self):
        now = time.monotonic()
        dt = min(now - self.last_time, 0.1)
        self.last_time = now

        if self.menu_active:
            return

        if self.intro_active or self.outro_active:
            return

        if self.day_screen.is_active(self.daynight.is_day()):
            self.day_screen_frames -= 1
            if self.day_screen_frames <= 0:
                self.day_screen.hide()
            return

        if self.game_over or self.game_finished:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0

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
                self.add_suspicion(dt, SUSPICION_TIME)
                return

            npc, evidence = self.get_npc_that_sees_evidence()
            if npc and evidence:
                self.add_suspicion(dt, EVIDENCE_SUSPICION_TIME)

    def get_npc_that_sees_player(self):
        # нпс который видит игрока
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

    def draw(self):
        if self.menu_active:
            self.menu_screen.draw(self.screen, self.title_font, self.font)
            pygame.display.flip()
            return

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
        if self.daynight.is_night():
            for npc in self.npcs:
                npc.draw_vision(self.screen, camera_x, camera_y)

        for npc in self.npcs:
            npc.draw(self.screen, self.font, camera_x, camera_y)
        for evidence in self.evidences:
            evidence.draw(self.screen, camera_x, camera_y)
        self.player.draw(self.screen, camera_x, camera_y)
        self.hud.draw(self.screen, self.font, self)
        self.scanner_ui.draw(self.screen, self.font)

        pygame.display.flip()
