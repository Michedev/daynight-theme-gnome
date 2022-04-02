from typing import Iterator, Tuple
from collections import OrderedDict
from daynight_theme.commands import GnomeThemeSetter, GnomeShellThemeSetter, PycharmThemeSetter, \
    BitDayBackground
from daynight_theme.commands.command import Command
from daynight_theme.commands.notification import SendNotification
from daynight_theme.sunrise_sunset_api import SunriseSunsetData
import numpy as np

_register_class = list()
_register_priority = list()


def register_command(priority: int = 0):
    def decorator(class_: Command):
        _register_class.append((class_.__name__, class_))
        _register_priority.append(priority)


def iter_commands() -> Iterator[Tuple[str, Command]]:
    i_sorted = np.argsort(_register_priority)
    for i in i_sorted:
        yield _register_class[i]
