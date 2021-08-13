import os

from daynight_theme.commands.command import Command


class GnomeShellThemeSetter(Command):

    def __init__(self, config):
        super().__init__(config)
        self.day_theme = config['day_theme']
        self.night_theme = config['night_theme']

    @staticmethod
    def can_add_to_registry(config):
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


class GnomeThemeSetter(Command):

    def __init__(self, config: dict):
        super().__init__(config)
        self.day_theme = config['day_shell_theme']
        self.night_theme = config['night_shell_theme']

    @staticmethod
    def can_add_to_registry(config) -> bool:
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
