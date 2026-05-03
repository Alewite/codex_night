import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, DARK_GRAY
from .player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("кодекс ночи")


        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(100,100)  # Создаем игрока в нач позиции

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
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.player.draw(self.screen)
        pygame.display.flip()