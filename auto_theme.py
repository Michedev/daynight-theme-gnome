from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Callable, List, Literal

from dateutil.parser import parse
from path import Path
import yaml
import time
import os

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
REQUIRED_FIELDS = ['day_theme', 'night_theme', 'day_start', 'day_end']
OPTIONAL_FIELDS = ['day_shell_theme', 'night_shell_theme']


def set_shell_theme_cmd(theme):
    return f'gsettings set org.gnome.shell.extensions.user-theme name "{theme}"'


def set_theme_cmd(theme: str):
    return f'gsettings set org.gnome.desktop.interface gtk-theme "{theme}"'


@dataclass
class Command:
    day_value: str
    night_value: str
    cmd_f: Callable


class CommandRunner:

    def __init__(self, commands: List[Command], day_start: time, day_end: time):
        self.day_start = day_start
        self.day_end = day_end
        self.commands = commands

    def loop_forever(self):
        while True:
            field = self.get_cmd_field()
            self.exec_commands(field)
            time.sleep(10 * 60 * 1000)  # 10 minutes

    def exec_commands(self, field: Literal['day_value', 'night_value']):
        for command in self.commands:
            field_value = getattr(command, field)
            cmd = command.cmd_f(field_value)
            os.system(cmd)

    def get_cmd_field(self) -> Literal['day_value', 'night_value']:
        curr_time = datetime.now()
        if self.day_start <= curr_time < self.day_end:
            return 'day_value'
        else:
            return 'night_value'


def load_config():
    assert USER_CONFIG.exists(), USER_CONFIG + ' doesn\'t exist'
    with open(USER_CONFIG) as f:
        config: dict = yaml.safe_load(f)
    for field in REQUIRED_FIELDS:
        assert field in config, f'required field {field} not in config {config}'
    config['day_start'], config['day_end'] = parse(config['day_start']), parse(config['day_end'])
    return config


def make_commands(config: dict) -> List[Command]:
    result = [
        Command(config['day_theme'], config['night_theme'], set_theme_cmd)
    ]
    if 'day_shell_theme' in config and 'night_shell_theme' in config:
        result.append(Command(config['day_shell_theme'], config['night_shell_theme'], set_shell_theme_cmd))
    return result


def main():
    config = load_config()
    commands = make_commands(config)
    runner = CommandRunner(commands, config['day_start'], config['day_end'])
    runner.loop_forever()


if __name__ == "__main__":
    main()
