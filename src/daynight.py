from .settings import DAY, NIGHT, MAX_DAYS


class DayNightManager:
    def __init__(self):
        self.phase = DAY
        self.day = 1

    def change_phase(self):
        if self.phase == DAY:
            self.phase = NIGHT
        else:
            self.phase = DAY
            if self.day < MAX_DAYS:
                self.day += 1

    def is_day(self):
        return self.phase == DAY

    def is_night(self):
        return self.phase == NIGHT

    def get_text(self):
        return f"{self.phase} {self.day}/{MAX_DAYS}"
