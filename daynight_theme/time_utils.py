import datetime
import numpy as np

def time_seconds(t: datetime.time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


def get_delta_seconds(t1: datetime.time, t2: datetime.time) -> int:
    delta = time_seconds(t1) - time_seconds(t2)
    if delta < 0:
        delta = 24 * 3600 + delta
    return delta


def get_dayphase(t: datetime.time, day_start: datetime.time, day_end: datetime.time):
    t_seconds: int = time_seconds(t)
    day_start_seconds: int = time_seconds(day_start)
    day_end_seconds: int = time_seconds(day_end)

    day_night_delta: int = get_delta_seconds(day_end, day_start)
    night_day_delta: int = get_delta_seconds(day_start, day_end)

    is_day = day_start_seconds <= t_seconds <= day_end_seconds
    t0 = day_start if is_day else day_end
    delta: int = day_night_delta if is_day else night_day_delta
    spans = np.linspace(0, delta, 4)

    t_seconds_fixed = get_delta_seconds(t, t0)

    for i in range(len(spans)-1):
        if spans[i] <= t_seconds_fixed <= spans[i+1]:
            return i


