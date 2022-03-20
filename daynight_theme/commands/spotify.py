import os

from daynight_theme.commands.command import Command


class SpotifyTheme(Command):

    @property
    def day_value(self) -> str:
        return 'gray-light'

    @property
    def night_value(self) -> str:
        return 'gray-dark'

    def action(self, value: str):
        os.system('spicetify config current_theme Ziro')
        os.system(f'spicetify config color_scheme {value}')
        os.system('spicetify apply')

    @staticmethod
    def is_runnable(config) -> bool:
        return os.system('spicetify') == 0 and config['spotify']