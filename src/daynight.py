import time
from .settings import DAY, NIGHT, MAX_NIGHTS


class DayNightManager:
    def __init__(self):
        self.phase = DAY
        self.night = 1
        self.start_time = time.monotonic()

    def update(self):
        pass

    def change_phase(self):
        if self.phase == DAY:
            self.phase = NIGHT
        else:
            self.phase = DAY
            if self.night < MAX_NIGHTS:
                self.night += 1

        # запоминаем время старта новой фазы
        self.start_time = time.monotonic()

    def is_day(self):
        return self.phase == DAY

    def is_night(self):
        return self.phase == NIGHT

    def get_text(self):
        return f"{self.phase} {self.night}/{MAX_NIGHTS}"
