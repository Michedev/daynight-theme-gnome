import os
from dataclasses import dataclass
from typing import Callable

from path import Path

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
REQUIRED_FIELDS = ['day_theme', 'night_theme', 'day_start', 'day_end']
OPTIONAL_FIELDS = ['day_shell_theme', 'night_shell_theme']


@dataclass
class Command:
    day_value: str
    night_value: str
    cmd_f: Callable