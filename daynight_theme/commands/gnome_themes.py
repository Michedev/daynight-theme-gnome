import os
from typing import NoReturn

from path import Path
from rich.prompt import Confirm, IntPrompt

from daynight_theme.command_register import register_command
from daynight_theme.commands.command import Command


def gtk_themes():
    theme_folder = Path(os.environ['HOME']) / '.themes'
    themes_list = [str(d.basename()) for d in theme_folder.dirs()]
    return themes_list


def gnome_shell_themes() -> list:
    root = Path(os.environ['HOME']) / '.themes'
    return [str(folder.basename()) for folder in root.dirs() if (folder / 'gnome-shell') in folder.dirs()]


def pick(choices: list, end_msg: str = None):
    msg = ""
    for i, v in enumerate(choices):
        msg += f'{i + 1}) {v}\n'
    if end_msg: msg += f'{end_msg}\n'
    int_choices = [str(x) for x in range(1, len(choices) + 1)]
    picked = IntPrompt.ask(msg, choices=int_choices, show_choices=False)
    return choices[picked - 1]

@register_command(priority=0)
class GnomeShellThemeSetter(Command):

    def __init__(self, config):
        super().__init__(config)
        self.day_theme = config['day_theme']
        self.night_theme = config['night_theme']

    @staticmethod
    def is_runnable(config):
        return 'day_theme' in config and 'night_theme' in config

    @property
    def day_value(self) -> str:
        return self.day_theme

    @property
    def night_value(self) -> str:
        return self.night_theme

    def action(self, value: str):
        cmd = f'gsettings set org.gnome.desktop.interface gtk-theme "{value}"'
        print(f'executing command "{cmd}"')
        os.system(cmd)

    @staticmethod
    def on_config_setup(config) -> NoReturn:
        themes_list = gtk_themes()
        day_theme_msg = 'Pick Gnome theme chosen during the day'
        night_theme_msg = 'Pick Gnome theme chosen during the night'
        print()
        day_theme = pick(themes_list, day_theme_msg)
        themes_list.remove(day_theme)
        print()
        night_theme = pick(themes_list, night_theme_msg)
        return str(day_theme), str(night_theme)


@register_command(priority=1)
class GnomeThemeSetter(Command):

    def __init__(self, config: dict):
        super().__init__(config)
        self.day_theme = config['day_shell_theme']
        self.night_theme = config['night_shell_theme']

    @staticmethod
    def is_runnable(config) -> bool:
        return 'day_shell_theme' in config and 'night_shell_theme' in config

    @property
    def day_value(self) -> str:
        return self.day_theme

    @property
    def night_value(self) -> str:
        return self.night_theme

    def action(self, value: str):
        cmd = f'gsettings set org.gnome.shell.extensions.user-theme name "{value}"'
        print(f'executing command "{cmd}"')
        os.system(cmd)

    @staticmethod
    def on_config_setup(config):
        add_shell_theme = Confirm.ask("Do you want to enter gnome shell theme too? [yes/no]")
        if add_shell_theme:
            day_theme_msg = 'Pick Gnome shell theme chosen during the day'
            night_theme_msg = 'Pick Gnome shell theme chosen during the night'
            themes_list = gnome_shell_themes()
            day_shell_theme = pick(themes_list, day_theme_msg)
            themes_list.remove(day_shell_theme)
            night_shell_theme = pick(themes_list, night_theme_msg)
            config['day_shell_theme'] = day_shell_theme
            config['night_shell_theme'] = night_shell_theme
