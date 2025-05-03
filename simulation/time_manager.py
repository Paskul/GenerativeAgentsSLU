# simulation/time_manager.py

from datetime import datetime, timedelta

class TimeManager:
    # manages sim time and increments to follow after start
    def __init__(self, start_time=None, time_step=timedelta(minutes=1)):
        if start_time is not None:
            self.current_time = start_time
        else:
            now = datetime.now()
            self.current_time = datetime(now.year, now.month, now.day, 6, 0, 0, 0)
        self.time_step = time_step

    def advance(self):
        self.current_time += self.time_step
        return self.current_time
