import time
from .settings import DAY_TIME, NIGHT_TIME, DAY, NIGHT
class DayNightManager:
    def __init__(self):
        self.phase = DAY
        self.day = 1
        self.start_time = time.monotonic()
    def update(self):
        if self.get_time_left() <= 0:
            self.cnange_phase()
    def cnange_phase(self):
        if self.phase == DAY:
            self.phase = NIGHT
        else:
            self.phase = DAY
            self.day += 1
        self.start_time = time.monotonic()
    def get_time_left(self):
        if self.phase == DAY:
            time_limit = DAY_TIME
        else:
            time_limit = NIGHT_TIME
        time_passed = time.monotonic() - self.start_time
        return max(0, time_limit - time_passed)
    def is_day(self):
        return self.phase == DAY
    def is_night(self):
        return self.phase == NIGHT
    def get_text(self):
        return f"{self.phase} {self.day} | {int(self.get_time_left())}"