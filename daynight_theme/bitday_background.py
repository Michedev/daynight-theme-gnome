import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time

import numpy as np
from path import Path

from daynight_theme.command import Command
from daynight_theme.sunrise_sunset_api import SunriseSunsetData

def to_datetime(t: time) -> datetime:
    return datetime(2000, 1, 1,
                    t.hour,
                    t.minute,
                    t.second)

@dataclass
class BitDayBackground(Command):
    sunrise_sunset: SunriseSunsetData = field(init=True)
    day_value: str = field(default='day', init=False)
    night_value: str = field(default='night', init=False)

    def __post_init__(self):
        day_spans = np.linspace(0, self.sunrise_sunset.delta_sunset_sunrise_seconds, 7)[1:]
        night_spans = np.linspace(0, self.sunrise_sunset.delta_sunrise_sunset_seconds, 7)[1:]
        self.max_diff_second_sunrise_sunset = max(self.sunrise_sunset.delta_sunset_sunrise_seconds,
                                                  self.sunrise_sunset.delta_sunrise_sunset_seconds)
        sunrise_dt = self.sunrise_sunset.sunrise
        sunset_dt = self.sunrise_sunset.sunset
        sunrise_dt = datetime(2000, 1, 1,
                              sunrise_dt.hour,
                              sunrise_dt.minute,
                              sunrise_dt.second)
        sunset_dt = datetime(2000, 1, 1,
                             sunset_dt.hour,
                             sunset_dt.minute,
                             sunset_dt.second)

        self.day_spans = [(sunrise_dt + timedelta(seconds=v)).time() for v in day_spans]
        self.night_spans = [(sunset_dt + timedelta(seconds=v)).time() for v in night_spans]
        self.day_images = ['./01-Early-Morning.png',
                           './02-Mid-Morning.png',
                           './03-Late-Morning.png',
                           './04-Early-Afternoon.png',
                           './05-Mid-Afternoon.png',
                           './06-Late-Afternoon.png']

        self.night_images = ['./07-Early-Evening.png',
                             './08-Mid-Evening.png',
                             './09-Late-Evening.png',
                             './10-Early-Night.png',
                             './11-Mid-Night.png',
                             './12-Late-Night.png']
        prefix = Path('/home/mikedev/Pictures/bitday_1920x1080')
        self.day_images = [prefix / x for x in self.day_images]
        self.night_images = [prefix / x for x in self.night_images]

    def action(self, value: str):
        time_spans = self.day_spans if value == 'day' else self.night_spans
        cur_time = datetime.now().time()
        if value == 'night':
            time_spans = [(to_datetime(t) - timedelta(hours=12)).time() for t in time_spans]
            cur_time = (to_datetime(cur_time) - timedelta(hours=12)).time()
        images = self.day_images if value == 'day' else self.night_images
        imgpath = self._find_background_image(images, time_spans, cur_time)
        print('set', str(imgpath))
        cmd = self._cmd_background(imgpath.abspath())
        os.system(cmd)

    def _find_background_image(self, images, time_spans, cur_time) -> Path:
        for i in range(len(time_spans)):
            time_span = time_spans[i]
            if time_span > cur_time:
                return images[i]

    def _cmd_background(self, imgpath: str) -> str:
        return f"gsettings set org.gnome.desktop.background picture-uri file://{imgpath}"
