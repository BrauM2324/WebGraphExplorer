import time


class TimeTracker:
    def __init__(self):
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start(self):
        self.start_time = time.perf_counter()
        self.end_time = None

    def end(self) -> float:
        if self.start_time is None:
            return 0.0
        self.end_time = time.perf_counter()
        return self.elapsed_time()

    def elapsed_time(self) -> float:
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else time.perf_counter()
        return round(end - self.start_time, 4)
