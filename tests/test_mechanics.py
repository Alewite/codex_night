import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

from src.collisions import BLOCK_ZONES, move_with_collisions, rect_collides
from src.game import Game
from src.npc import create_npcs_for_day
from src.settings import MAX_DAYS, NPC_SIZE, SUSPICION_TIME
from src.suspicion import Suspicion


class MechanicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_player_does_not_move_inside_collision(self):
        block_zone = BLOCK_ZONES[1]
        rect = pygame.Rect(
            block_zone.left - NPC_SIZE,
            block_zone.top,
            NPC_SIZE,
            NPC_SIZE,
        )

        old_x = rect.x
        blocked = move_with_collisions(rect, 1, 0, 10)

        self.assertTrue(blocked)
        self.assertEqual(rect.x, old_x)

    def test_npcs_spawn_outside_collisions(self):
        for day in range(1, MAX_DAYS + 1):
            for npc in create_npcs_for_day(day):
                self.assertFalse(rect_collides(npc.rect))

    def test_suspicion_reaches_max(self):
        suspicion = Suspicion()
        is_full = suspicion.add(SUSPICION_TIME, SUSPICION_TIME)

        self.assertTrue(is_full)
        self.assertEqual(suspicion.percent(), 100)

    def test_deposit_evidence_increases_counter(self):
        game = Game()
        game.carried_evidence = 2
        game.delivered_evidence = 1

        game.interactions.deposit_evidence()

        self.assertEqual(game.carried_evidence, 0)
        self.assertEqual(game.delivered_evidence, 3)

    def test_game_finishes_after_last_evidence(self):
        game = Game()
        game.carried_evidence = 1
        game.criminals_done = MAX_DAYS

        game.interactions.deposit_evidence()

        self.assertTrue(game.game_finished)
        self.assertTrue(game.outro_active)


if __name__ == "__main__":
    unittest.main()
