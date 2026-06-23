from .settings import MAX_DAYS
from .objects import Evidence


class InteractionManager:
    def __init__(self, game):
        self.game = game

    def handle_action(self):
        # действие e не работает после конца игры
        if self.game.game_over or self.game.game_finished:
            return

        if self.game.scanner_ui.active:
            return

        if self.game.house.is_near_player(self.game.player):
            self.change_phase_near_house()
            return

        if self.collect_near_evidence():
            return

        if self.game.boat.is_near_player(self.game.player) and self.game.carried_evidence > 0:
            self.deposit_evidence()
            return

        # сканирование только днем
        if self.game.daynight.is_day():
            self.scan_near_npc()

    def has_criminal(self):
        for npc in self.game.npcs:
            if npc.is_criminal:
                return True
        return False

    def change_phase_near_house(self):
        # днем дом переводит игру в ночь
        if self.game.daynight.is_day():
            self.game.daynight.change_phase()
            self.game.audio.play_phase_sound(self.game.daynight.is_night())
            self.game.message = ""
            return

        if self.has_criminal():
            self.game.message = "сначала устраните преступника"
            return

        if self.game.evidences or self.game.carried_evidence > 0:
            self.game.message = "сначала сбросьте улику"
            return

        if self.game.daynight.day < MAX_DAYS:
            self.game.daynight.change_phase()
            self.game.audio.play_phase_sound(self.game.daynight.is_night())
            self.game.spawn_npcs()
            self.game.show_day_screen()
            self.game.message = ""

    def eliminate_near_criminal(self):
        # убийство доступно только ночью
        if self.game.game_over or self.game.game_finished:
            return

        if not self.game.daynight.is_night():
            return

        for npc in self.game.npcs[:]:
            if npc.is_near_player(self.game.player) and npc.is_criminal and npc.is_scanned:
                evidence = Evidence(npc.rect.centerx, npc.rect.centery)
                self.game.evidences.append(evidence)
                self.game.npcs.remove(npc)
                self.game.criminals_done += 1
                self.game.audio.play_kill_sound()
                self.game.message = "цель устранена"
                break

    def collect_near_evidence(self):
        for evidence in self.game.evidences[:]:
            if evidence.is_near_player(self.game.player):
                self.game.carried_evidence += 1
                self.game.evidences.remove(evidence)
                return True

        return False

    def deposit_evidence(self):
        self.game.delivered_evidence += self.game.carried_evidence
        self.game.carried_evidence = 0

        if self.game.criminals_done >= MAX_DAYS:
            self.game.finish_game()

    def scan_near_npc(self):
        for npc in self.game.npcs:
            if npc.is_near_player(self.game.player):
                npc.scan()
                self.game.scanner_ui.open(npc)
                self.game.audio.play_scanner_sound()
                break
