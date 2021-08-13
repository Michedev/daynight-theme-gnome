from typing import Iterator, Tuple

from daynight_theme.commands import GnomeThemeSetter, GnomeShellThemeSetter, PycharmThemeSetter, \
    PycharmColorSetter, BitDayBackground
from daynight_theme.commands.command import Command
from daynight_theme.commands.notification import SendNotification
from daynight_theme.sunrise_sunset_api import SunriseSunsetData

_register = dict()


def get_command(k: str): return _register[k]


def set_command(k: str, c: Command):
    assert isinstance(c, Command)
    _register[k] = c


def init_register(config: dict):
    CMD_THEME = GnomeThemeSetter(config)
    set_command('gnome_theme', CMD_THEME)
    if GnomeShellThemeSetter.can_add_to_registry(config):
        CMD_SHELL = GnomeShellThemeSetter(config)
        set_command('gnome_shell_theme', CMD_SHELL)
    if PycharmColorSetter.can_add_to_registry(config):
        PYCHARM_THEME_CMD = PycharmThemeSetter(config)
        PYCHARM_COLOR_CMD = PycharmColorSetter(config)
        set_command('pycharm_theme', PYCHARM_THEME_CMD)
        set_command('pycharm_color', PYCHARM_COLOR_CMD)
    if BitDayBackground.can_add_to_registry(config):
        b = BitDayBackground(config)
        set_command('bitday_background', b)
    cmd_notification = SendNotification(config)
    set_command('daynight_notification', cmd_notification)


def iter_commands() -> Iterator[Command]:
    yield from _register.values()


def iter_cmd_keys() -> Iterator[str]:
    yield from _register.keys()


def iter_keys_commands() -> Iterator[Tuple[str, Command]]:
    yield from _register.items()
