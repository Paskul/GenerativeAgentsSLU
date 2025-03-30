from datetime import datetime, timedelta

class TimeManager:
    def __init__(self, start_time: datetime = None, time_step: timedelta = timedelta(minutes=1)):
        # start_time we can set as a real day if needed, otherwise defaults to 6:00 AM
        # time_step is how much it forwards by in each clock step
        if start_time is not None:
            self.current_time = start_time
        else:
            now = datetime.now()
            self.current_time = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=6,
                minute=0,
                second=0,
                microsecond=0
            )
        self.time_step = time_step

    def advance(self) -> datetime:
        self.current_time += self.time_step
        return self.current_time
