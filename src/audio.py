import os

import pygame

from .settings import (
    DAY_SOUND_PATH,
    NIGHT_SOUND_PATH,
    SCANNER_SOUND_PATH,
    KILL_SOUND_PATH,
)


class AudioManager:
    def __init__(self):
        self.day_sound = self.load_sound(DAY_SOUND_PATH)
        self.night_sound = self.load_sound(NIGHT_SOUND_PATH)
        self.scanner_sound = self.load_sound(SCANNER_SOUND_PATH)
        self.kill_sound = self.load_sound(KILL_SOUND_PATH)
        self.phase_channel = None

    def load_sound(self, path):
        if not os.path.exists(path):
            return None

        try:
            # mixer для коротких звуков
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None

    def play_sound(self, sound):
        # проигрываем эффект если он загрузился
        if not sound:
            return

        try:
            sound.play()
        except pygame.error:
            pass

    def play_scanner_sound(self):
        self.play_sound(self.scanner_sound)

    def play_kill_sound(self):
        self.play_sound(self.kill_sound)

    def stop_phase_sound(self):
        if self.phase_channel:
            self.phase_channel.stop()
            self.phase_channel = None

    def play_phase_sound(self, is_night):
        self.stop_phase_sound()

        if is_night:
            sound = self.night_sound
        else:
            sound = self.day_sound

        if not sound:
            return

        try:
            # запуск звука дня или ночи по кругу
            self.phase_channel = sound.play(-1)
        except pygame.error:
            self.phase_channel = None
