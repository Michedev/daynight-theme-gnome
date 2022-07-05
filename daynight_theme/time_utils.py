import datetime
from typing import List

import numpy as np

def time_seconds(t: datetime.time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


def get_delta_seconds(t1: datetime.time, t2: datetime.time) -> int:
    delta = time_seconds(t1) - time_seconds(t2)
    if delta < 0:
        delta = 24 * 3600 + delta
    return delta


def get_dayphase(t: datetime.time, day_start: datetime.time, day_end: datetime.time, spans: List[float] = None):
    if spans is None:
        spans = [0.33, 0.34, 0.33]
    assert all(x >= 0 for x in spans), spans
    sum_spans = sum(spans)
    if sum_spans != 1.0:
        spans = [x / sum_spans for x in spans]
    cum_spans = [spans[0]]
    for i in range(len(spans)-1):
        cum_spans.append(cum_spans[-1] + spans[i+1])
    t_seconds: int = time_seconds(t)
    day_start_seconds: int = time_seconds(day_start)
    day_end_seconds: int = time_seconds(day_end)

    day_night_delta: int = get_delta_seconds(day_end, day_start)
    night_day_delta: int = get_delta_seconds(day_start, day_end)

    is_day = day_start_seconds <= t_seconds <= day_end_seconds
    t0 = day_start if is_day else day_end
    delta: int = day_night_delta if is_day else night_day_delta
    spans = [0.0] + [x * delta for x in cum_spans]

    t_seconds_fixed = get_delta_seconds(t, t0)

    for i in range(len(spans)-1):
        if spans[i] <= t_seconds_fixed <= spans[i+1]:
            return i


