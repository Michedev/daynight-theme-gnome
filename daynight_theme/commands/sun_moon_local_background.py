import datetime
import os
from random import shuffle
from typing import NoReturn

from path import Path

from daynight_theme import time_utils
from daynight_theme.gnome_utils import get_cmd_background
from daynight_theme.sunrise_sunset_api import SunriseSunsetData
from rich.prompt import Confirm
from rich import print as rich_print
import numpy as np
from pkg_resources import resource_filename

from daynight_theme.command_register import register_command
from daynight_theme.commands import Command

_key_on_off = 'sun_moon_background'

day_range = None
night_range = None


def get_data_path(phase: str):
    return resource_filename('daynight_theme', f'data/background/{phase}')


@register_command(priority=6)
class SunMoonLocalBackground(Command):
    day_phases = ['sunrise', 'high_sun', 'sunfall']
    night_phases = ['early_moon', 'middle_moon', 'late_moon']

    def __init__(self, config: dict):
        super().__init__(config)
        self.day_start: datetime.time = config['day_start']
        self.day_end: datetime.time = config['day_end']
        self.sunset_data = SunriseSunsetData(self.day_start, self.day_end)

        self.day_duration_seconds: int = self.sunset_data.delta_sunrise_sunset_seconds
        self.night_duration_seconds: int = self.sunset_data.delta_sunset_sunrise_seconds
        self.day_spans = np.linspace(0, self.day_duration_seconds, 4)
        self.night_spans = np.linspace(0, self.night_duration_seconds, 4)

    @property
    def day_value(self) -> str:
        return "day"

    @property
    def night_value(self) -> str:
        return "night"

    def action(self, value: str):
        phases: list = self.day_phases if value == self.day_value else self.night_phases
        i_phase: int = time_utils.get_dayphase(datetime.datetime.now().time(), self.day_start, self.day_end, )
        phase: str = phases[i_phase]
        data_path = Path(get_data_path(phase))
        images = data_path.files()
        shuffle(images)
        newimage_path = images[0]
        os.system(get_cmd_background(newimage_path))

        rich_print('set wallpaper',  '[black]' + str(newimage_path).replace(phase, f'[underline][bold]{phase}[/bold][/underline]') + '[/black]')


    @staticmethod
    def is_runnable(config) -> bool:
        if _key_on_off not in config:
            return False
        return config[_key_on_off]

    @staticmethod
    def on_config_setup(config) -> NoReturn:
        if config['bitday_background']:
            enable_pixelart = Confirm.ask('Bitday background is enabled, do you want to disable it '
                                          'to enable sun/moon pixel art backgrounds? [yes/no]')
            config['bitday_background'] = not enable_pixelart
            config[_key_on_off] = enable_pixelart
        else:
            prompt = Confirm.ask("Do you want sun/moon background switch? [yes/no]")
            config[_key_on_off] = prompt
