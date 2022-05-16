import asyncio
import os

import yaml
from dateutil.parser import parse
from path import Path

from .command_register import iter_commands
from .command_runner import CommandRunner, update_sunrise_sunset_everyday
from .sunrise_sunset_api import sunrise_sunset_time


USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'


def load_config():
    assert USER_CONFIG.exists(), USER_CONFIG + ' doesn\'t exist'
    with open(USER_CONFIG) as f:
        config: dict = yaml.safe_load(f)
    if not config['use_api_sunrise_sunfall']:
        config['day_start'], config['day_end'] = parse(config['day_start']), parse(config['day_end'])
    else:
        daynight_api = sunrise_sunset_time(config['api_latitude'], config['api_longitude'])
        config['day_start'] = daynight_api.sunrise
        config['day_end'] = daynight_api.sunset
    return config


def main():
    config = load_config()
    commands = []
    for cmd_name, CmdClass in iter_commands():
        if CmdClass.is_runnable(config):
            commands.append(CmdClass(config))
    runner = CommandRunner(config['day_start'], config['day_end'], commands)
    if config['use_api_sunrise_sunfall']:
        asyncio.gather(update_sunrise_sunset_everyday(runner))
    runner.loop_forever()

if __name__ == '__main__':
    main()