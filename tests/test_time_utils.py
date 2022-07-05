import datetime

from daynight_theme.time_utils import get_delta_seconds, get_dayphase


def test_subtract_times_ahead_hours():
    a = datetime.time(5, 10, 5)
    b = datetime.time(23, 10, 5)
    assert get_delta_seconds(a, b) == 6 * 3600  # 6 hours


def test_subtract_times_normal():
    a = datetime.time(23, 10, 5)
    b = datetime.time(23, 10, 0)
    actual = get_delta_seconds(a, b)
    expected = 5
    assert actual == expected


def test_get_dayphase_night_start():
    t = datetime.time(21, 10, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end) == 0


def test_get_dayphase_night_end():
    t = datetime.time(4, 0, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end) == 2


def test_get_dayphase_day_start():
    t = datetime.time(5, 30, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end) == 0


def test_get_dayphase_day_end():
    t = datetime.time(19, 30, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end) == 2


def test_get_dayphase_day_end_different_spans():
    t = datetime.time(13, 30, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end, [0.1, 0.1, 0.8]) == 2


def test_get_dayphase_night_start_different_spans():
    t = datetime.time(13, 30, 5)

    day_start = datetime.time(5, 10, 0)
    day_end = datetime.time(20, 0, 0)

    assert get_dayphase(t, day_start, day_end, [0.8, 0.1, 0.1]) == 0
