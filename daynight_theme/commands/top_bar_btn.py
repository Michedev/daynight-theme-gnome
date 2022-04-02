from typing import NoReturn

from path import Path
from rich.prompt import Confirm, IntPrompt

from daynight_theme.command_register import register_command
from daynight_theme.commands.command import Command
import os

UNITE_PATH = Path(os.environ['HOME']) / '.local' / 'share' / 'gnome-shell' / 'extensions' / 'unite@hardpixel.eu'


def pick(choices: list, end_msg: str = None):
    msg = ""
    for i, v in enumerate(choices):
        msg += f'{i + 1}) {v}\n'
    if end_msg: msg += f'{end_msg}\n'
    int_choices = [str(x) for x in range(1, len(choices) + 1)]
    picked = IntPrompt.ask(msg, choices=int_choices, show_choices=False)
    return choices[picked - 1]


@register_command(6)
class TopBarBtn(Command):

    @staticmethod
    def is_runnable(config) -> bool:
        return UNITE_PATH.exists() and config['unite_button']

    @property
    def day_value(self) -> str:
        key = 'unite_daybutton'
        return self.config[key] if key in self.config else 'united-dark'

    @property
    def night_value(self) -> str:
        key = 'unite_nightbutton'
        return self.config[key] if key in self.config else 'united-light'

    def action(self, value: str):
        value = f"""  "'{value}'"  """.strip()
        os.system(f'dconf write /org/gnome/shell/extensions/unite/window-buttons-theme {value}')

    @staticmethod
    def on_config_setup(config) -> NoReturn:
        if not UNITE_PATH.exists():
            print('Warning: Unite extension not found at path', str(UNITE_PATH))
            return False, None
        use_unite = Confirm.ask('Do you want to switch day night unite buttons? [yes/no]')
        if use_unite:
            pick_unite_theme = Confirm.ask('Do you want to choose button theme? [default is united-dark/united-light]')
            if pick_unite_theme:
                theme_list = [x.basename for x in (UNITE_PATH / 'themes').dirs()]
                day_theme = pick(theme_list, 'Select day button theme:')
                print()
                theme_list.remove(day_theme)
                night_theme = pick(theme_list, 'Select night button theme:')
            else:
                day_theme = 'united-dark'
                night_theme = 'united-light'
            config['unite_button'] = use_unite
            config['unite_daybutton'] = day_theme
            config['unite_nightbutton'] = night_theme
