import os

from daynight_theme.command import Command


class GnomeShellThemeSetter(Command):

    def __init__(self, day_theme: str, night_theme: str):
        self.day_value = day_theme
        self.night_value = night_theme

    def action(self, value: str):
        cmd = f'gsettings set org.gnome.shell.extensions.user-theme name "{value}"'
        os.system(cmd)


class GnomeThemeSetter(Command):

    def __init__(self, day_theme: str, night_theme: str):
        self.day_value = day_theme
        self.night_value = night_theme

    def action(self, value: str):
        cmd = f'gsettings set org.gnome.desktop.interface gtk-theme "{value}"'
        os.system(cmd)
