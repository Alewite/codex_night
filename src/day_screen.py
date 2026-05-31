import time

from .settings import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, DAY_TEXT_TIME


class DayScreen:
    def __init__(self):
        self.text = ""
        self.start_time = 0

    def show(self, night):
        self.text = f"ДЕНЬ {night}"
        self.start_time = time.monotonic()

    def is_active(self, is_day):
        if not self.text:
            return False

        if not is_day:
            return False

        return time.monotonic() - self.start_time <= DAY_TEXT_TIME

    def draw(self, screen, font):
        screen.fill(BLACK)

        text = font.render(self.text, True, WHITE)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (x, y))
