import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, DARK_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, YELLOW,  WORLD_WIDTH, WORLD_HEIGHT
from .player import Player
from .world import World
from .npc import NPC
from .ui import ScannerUI
from .daynight import DayNightManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("кодекс ночи")


        self.clock = pygame.time.Clock()
        self.running = True
        self.world = World()
        self.player = Player(100,100)  # Создаем игрока в нач позиции
        self.font = pygame.font.SysFont("arial", 18)

        self.npcs = [
        NPC("Mark", 400, 280, True),
        NPC("Anna", 600, 350, False),
        NPC("Leo", 250, 250),
        ]
        self.scanner_ui = ScannerUI()
        self.daynight = DayNightManager()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    def get_camera(self):
        camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
        return camera_x, camera_y 
    # выход через крестик и esc
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.scan_near_npc()
                if event.key == pygame.K_ESCAPE:
                    if self.scanner_ui.active:
                        self.scanner_ui.close()
                    else:
                        self.running = False
    def scan_near_npc(self):
        for npc in self.npcs:
            if npc.is_near_player(self.player):
                npc.scan()
                self.scanner_ui.open(npc)
                break     
 # ходьба WASD игрока
    def update(self):
        self.daynight.update()
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
            npc.update()
    def draw_daynight_info(self):
        text = self.font.render(self.daynight.get_text(), True, YELLOW)
        self.screen.blit(text, (20, 20))
    def draw_night_overlay(self):
        if self.daynight.is_night():
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
    def draw(self):
        camera_x, camera_y = self.get_camera()

        self.world.draw(
            self.screen,
            camera_x,
            camera_y,
            self.daynight.is_night()
            )
        for npc in self.npcs:
            npc.draw(self.screen, self.font, camera_x, camera_y)
        
        self.player.draw(self.screen, camera_x, camera_y)

        self.draw_daynight_info()
        for npc in self.npcs:
            if npc.is_near_player(self.player) and not self.scanner_ui.active:
                self.scanner_ui.draw_hint(self.screen, self.font)
                break
        self.scanner_ui.draw(self.screen, self.font)
        pygame.display.flip()