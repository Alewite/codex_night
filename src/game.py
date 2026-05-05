import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, DARK_GRAY
from .player import Player
from .world import World
from .npc import NPC

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

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
    # выход через крестик и esc
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.scan_near_npc()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    def scan_near_npc(self):
        for npc in self.npcs:
            if npc.is_near_player(self.player):
                npc.scan()
                break     
 # ходьба WASD игрока
    def update(self):
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

    def draw(self):
        self.world.draw(self.screen)
        for npc in self.npcs:
            npc.draw(self.screen, self.font)
        
        self.player.draw(self.screen)
        pygame.display.flip()