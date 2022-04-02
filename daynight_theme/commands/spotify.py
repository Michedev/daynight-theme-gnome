import os

from rich.prompt import Confirm

from daynight_theme.command_register import register_command
from daynight_theme.commands.command import Command


@register_command(5)
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

    @staticmethod
    def on_config_setup(config) -> bool:
        spotify = Confirm.ask('Do you want day/night spotify themes? (this will download spicetify) [yes/no]')
        config['spotify'] = spotify
        if spotify:
            os.system('curl -fsSL https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.sh | sh')
            os.system('git clone https://github.com/spicetify/spicetify-themes.git')
            os.system('cd spicetify-themes && cp -r * ~/.config/spicetify/Themes && cd .. && rm -rf spicetify-themes')