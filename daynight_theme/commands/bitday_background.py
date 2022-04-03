import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from typing import NoReturn

import numpy as np
from path import Path
from rich.prompt import Confirm

from daynight_theme.command_register import register_command
from daynight_theme.commands.command import Command
from daynight_theme.sunrise_sunset_api import SunriseSunsetData

BITDAY_PREFIX = Path(os.environ["HOME"]) / 'Pictures' / 'bitday'


def to_datetime(t: time) -> datetime:
    return datetime(2000, 1, 1,
                    t.hour,
                    t.minute,
                    t.second)


def _download_bitday_images():
    import zipfile
    os.chdir(Path(os.environ['HOME']) / 'Pictures')
    dst_folder = Path('bitday')
    if dst_folder.exists():
        dst_folder.rmtree()
    dst_folder.mkdir()
    with zipfile.ZipFile('./BitDay-2-1920x1080.zip', 'r') as f:
        f.extractall(dst_folder)
    (dst_folder / '__MACOSX').rmtree()
    images_folder: Path = dst_folder / '1920x1080'
    for img in images_folder.files('*.png'):
        img.move(dst_folder)
    images_folder.rmtree()
    print('Put bitday images into', dst_folder.abspath())


@register_command(priority=3)
class BitDayBackground(Command):

    asap_update: bool = True

    def __init__(self, config: dict):
        super().__init__(config)
        self.sunrise_sunset = SunriseSunsetData(config['day_start'], config['day_end'])
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
        self.day_images = ['01-Early-Morning.png',
                           '02-Mid-Morning.png',
                           '03-Late-Morning.png',
                           '04-Early-Afternoon.png',
                           '05-Mid-Afternoon.png',
                           '06-Late-Afternoon.png']

        self.night_images = ['07-Early-Evening.png',
                             '08-Mid-Evening.png',
                             '09-Late-Evening.png',
                             '10-Early-Night.png',
                             '11-Mid-Night.png',
                             '12-Late-Night.png']
        self.day_images = [BITDAY_PREFIX / x for x in self.day_images]
        self.night_images = [BITDAY_PREFIX / x for x in self.night_images]

    @property
    def day_value(self) -> str:
        return 'day'

    @property
    def night_value(self) -> str:
        return 'night'

    @staticmethod
    def is_runnable(config) -> bool:
        return config['bitday_background']

    #todo: add tests
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

    @staticmethod
    def on_config_setup(config) -> NoReturn:
        bitday_background = Confirm.ask('Do you want bitday background? [yes/no]')
        if bitday_background:
            _download_bitday_images()
            config['bitday_background'] = bitday_background

