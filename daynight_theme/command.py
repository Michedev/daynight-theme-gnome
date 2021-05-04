import os
from abc import ABC, abstractmethod

from path import Path

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
REQUIRED_FIELDS = ['day_theme', 'night_theme', 'day_start', 'day_end']
OPTIONAL_FIELDS = ['day_shell_theme', 'night_shell_theme']


class Command(ABC):
    day_value: str
    night_value: str



    @abstractmethod
    def action(self, value: str):
        pass