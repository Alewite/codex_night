import os
import time
import wave

import pygame

from .settings import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, INTRO_TEXT_SPEED, STORY_TEXT_SPEED


INTRO_TEXT = (
    "Эта игра вдохновлена атмосферой сериала Декстер.\n\n"
    "Ты живешь по кодексу ночи. Днем город кажется спокойным, "
    "но среди обычных людей каждый день появляется один преступник.\n\n"
    "Днем нужно подходить к жителям города и нажимать E, чтобы сканировать их. "
    "Имя мирного станет зеленым, имя преступника станет красным.\n\n"
    "Ночью устрани только просканированного преступника клавишей F. "
    "После этого забери улику, отнеси ее к яхте и сбрось.\n\n"
    "Не попадайся в поле зрения жителей ночью. Подозреваемость копится всю игру. "
    "Если она дойдет до 100%, тебя рассекретят.\n\n"
    "Всего есть 5 ночей. Каждую ночь появляются новые 5 жителей, "
    "и среди них один новый преступник.\n\n"
)

OUTRO_TEXT = (
    "Пять ночей закончились.\n\n"
    "Майами снова делает вид, что он чист. "
    "Утром улицы блестят на солнце, люди улыбаются, "
    "и никто не спрашивает, почему ночь стала такой тихой.\n\n"
    "Кодекс не делает меня героем. Он просто держит тьму на поводке.\n\n"
    "Пятеро исчезли. Пять следов ушли в воду. "
    "Город получил еще один шанс проснуться без страха.\n\n"
    "Иногда порядок выглядит как обычный рассвет.\n\n"
)


class StoryScreen:
    def __init__(self, title, text, hint, audio_path=None):
        self.title = title
        self.text = text
        self.hint = hint
        self.audio_path = audio_path
        self.audio_duration = self.get_audio_duration()
        self.text_speed = self.get_text_speed()
        self.audio_playing = False
        self.start_time = time.monotonic()

    def get_audio_duration(self):
        if not self.audio_path or not os.path.exists(self.audio_path):
            return 0

        try:
            with wave.open(self.audio_path, "rb") as audio_file:
                return audio_file.getnframes() / audio_file.getframerate()
        except wave.Error:
            return 0

    def get_text_speed(self):
        if self.audio_duration > 0:
            return STORY_TEXT_SPEED

        return INTRO_TEXT_SPEED

    def restart(self):
        self.start_time = time.monotonic()
        self.stop_audio()
        self.play_audio()

    def play_audio(self):
        if not self.audio_path or not os.path.exists(self.audio_path):
            return

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()
            self.audio_playing = True
        except pygame.error:
            self.audio_playing = False

    def stop_audio(self):
        if not self.audio_playing:
            return

        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

        self.audio_playing = False

    def wrap_text(self, text, font, max_width):
        lines = []
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            if not paragraph:
                lines.append("")
                continue

            words = paragraph.split(" ")
            line = ""
            for word in words:
                test_line = word if not line else line + " " + word
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word

            if line:
                lines.append(line)

        return lines

    def draw(self, screen, title_font, font):
        screen.fill(BLACK)

        title = title_font.render(self.title, True, WHITE)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title, (title_x, 70))

        chars_count = int((time.monotonic() - self.start_time) * self.text_speed)
        visible_text = self.text[:chars_count]
        if chars_count < len(self.text):
            visible_text += "|"
        else:
            self.stop_audio()

        lines = self.wrap_text(visible_text, font, 760)
        y = 155
        for line in lines:
            text = font.render(line, True, WHITE)
            screen.blit(text, (120, y))
            y += 28

        if chars_count >= len(self.text):
            hint = font.render(self.hint, True, WHITE)
            hint_x = SCREEN_WIDTH // 2 - hint.get_width() // 2
            screen.blit(hint, (hint_x, SCREEN_HEIGHT - 55))
