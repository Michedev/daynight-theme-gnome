import asyncio
from typing import List

import yaml
from dateutil.parser import parse

from .command import USER_CONFIG, REQUIRED_FIELDS, Command
from .pycharm_daynight import exists_pycharm, PYCHARM_THEME_CMD, PYCHARM_COLOR_CMD
from .notification import CMD_NOTIFICATION
from .command_runner import CommandRunner, set_sunrise_sunset_everyday
from .bitday_background import BitDayBackground
from .gnome_themes import GnomeThemeSetter, GnomeShellThemeSetter
from .sunrise_sunset_api import SunriseSunsetData, sunrise_sunset_time


def load_config():
    assert USER_CONFIG.exists(), USER_CONFIG + ' doesn\'t exist'
    with open(USER_CONFIG) as f:
        config: dict = yaml.safe_load(f)
    for field in REQUIRED_FIELDS:
        assert field in config, f'required field {field} not in config {config}'
    config['day_start'], config['day_end'] = parse(config['day_start']), parse(config['day_end'])
    sun_time = sunrise_sunset_time()
    config['day_start'] = sun_time.sunrise
    config['day_end'] = sun_time.sunset
    return config


def make_commands(config: dict) -> List[Command]:
    CMD_THEME = GnomeThemeSetter(config['day_theme'], config['night_theme'])
    result: List[Command] = [
        CMD_THEME
    ]
    if 'day_shell_theme' in config and 'night_shell_theme' in config:
        CMD_SHELL = GnomeShellThemeSetter(config['day_shell_theme'], config['night_shell_theme'])
        result.append(CMD_SHELL)
    if 'pycharm' in config:
        if config['pycharm'] and exists_pycharm():
            result.append(PYCHARM_THEME_CMD)
            result.append(PYCHARM_COLOR_CMD)
    else:
        if exists_pycharm():
            result.append(PYCHARM_THEME_CMD)
            result.append(PYCHARM_COLOR_CMD)

    b = BitDayBackground(SunriseSunsetData(config['day_start'], config['day_end']))
    result.append(b)
    result.append(CMD_NOTIFICATION)
    return result


def main():
    config = load_config()
    commands = make_commands(config)
    runner = CommandRunner(commands, config['day_start'], config['day_end'])
    asyncio.gather(set_sunrise_sunset_everyday(runner))
    runner.loop_forever()