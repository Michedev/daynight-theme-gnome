import asyncio
from typing import List

from daynight_theme.command_runner import CommandRunner
from daynight_theme.gnome_themes import set_shell_theme_cmd, set_theme_cmd
from daynight_theme.pycharm_daynight import exists_pycharm, PYCHARM_COLOR_CMD, PYCHARM_THEME_CMD
from daynight_theme.notification import CMD_NOTIFICATION
import yaml
from dateutil.parser import parse

from daynight_theme.command import USER_CONFIG, REQUIRED_FIELDS, Command
from daynight_theme.sunrise_sunset_api import sunrise_sunset_time, set_sunrise_sunset_everyday


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
    CMD_THEME = Command(config['day_theme'], config['night_theme'], set_theme_cmd)
    result = [
        CMD_THEME
    ]
    if 'day_shell_theme' in config and 'night_shell_theme' in config:
        CMD_SHELL = Command(config['day_shell_theme'], config['night_shell_theme'], set_shell_theme_cmd)
        result.append(CMD_SHELL)
    if 'pycharm' in config:
        if config['pycharm'] and exists_pycharm():
            result.append(PYCHARM_THEME_CMD)
            result.append(PYCHARM_COLOR_CMD)
    else:
        if exists_pycharm():
            result.append(PYCHARM_THEME_CMD)
            result.append(PYCHARM_COLOR_CMD)
    result.append(CMD_NOTIFICATION)
    return result




def main():
    config = load_config()
    commands = make_commands(config)
    runner = CommandRunner(commands, config['day_start'], config['day_end'])
    asyncio.gather(set_sunrise_sunset_everyday(runner))
    runner.loop_forever()

if __name__ == "__main__":
    main()