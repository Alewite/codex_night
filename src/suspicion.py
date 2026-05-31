from .settings import SUSPICION_MAX


class Suspicion:
    def __init__(self):
        self.value = 0

    def reset(self):
        self.value = 0

    def add(self, dt, time_limit):
        self.value += (SUSPICION_MAX / time_limit) * dt

        if self.value >= SUSPICION_MAX:
            self.value = SUSPICION_MAX
            return True

        return False

    def percent(self):
        return int(self.value)
