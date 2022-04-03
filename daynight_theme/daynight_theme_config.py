import os
import re
from datetime import datetime, time
from itertools import chain
import yaml
from path import Path
from rich.prompt import IntPrompt, Confirm, FloatPrompt, Prompt

from daynight_theme.command_register import iter_commands

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
ROOT_THEMES = Path(os.environ['HOME']) / '.themes'
UNITE_PATH = Path(os.environ['HOME']) / '.local' / 'share' / 'gnome-shell' / 'extensions' / 'unite@hardpixel.eu'


def parse_time(msg):
    is_correct = False
    time_regex = '^$|([0-9]{1,2}:[0-9]{1,2})'
    matcher = re.compile(time_regex)
    hour, mins = None, None
    while not is_correct:
        try:
            m = matcher.match(input(msg))
            hour, mins = int(m.group(1)), int(m.group(2))
            is_correct = 0 <= hour < 24 and 0 <= mins < 60
        except:
            is_correct = False
        print('wrong input, it should be on the form HH:MM')
    t = time(hour, mins, 0)
    return t


def pick(choices: list, end_msg: str = None):
    msg = ""
    for i, v in enumerate(choices):
        msg += f'{i + 1}) {v}\n'
    if end_msg: msg += f'{end_msg}\n'
    int_choices = [str(x) for x in range(1, len(choices) + 1)]
    picked = IntPrompt.ask(msg, choices=int_choices, show_choices=False)
    return choices[picked - 1]


def gtk_themes():
    theme_folder = Path(os.environ['HOME']) / '.themes'
    themes_list = [d.basename() for d in theme_folder.dirs()]
    return themes_list

class SunriseSunSetDayNight:

    @staticmethod
    def on_config_setup(config):
        daytime_auto = Confirm.ask("Do you want to setup day/night time automatically based on your latitude/longitude [yes/no]")
        config['use_api_sunrise_sunfall'] = daytime_auto
        if daytime_auto:
            FLORENCE_LAT = 43.7799528
            FLORENCE_LONG = 11.2059486
            latitude = FloatPrompt.ask(f"Insert the latitude:", default=FLORENCE_LAT)
            longitude = FloatPrompt.ask(f"Inset the longitude:", default=FLORENCE_LONG)
            config['api_latitude'] = latitude
            config['api_longitude'] = longitude
        else:
            day_start = parse_time('insert day start time (HH:mm): ')
            day_end = parse_time('insert night start time (HH:mm): ')
            config['day_start'] = day_start
            config['day_end'] = day_end


def run_all_actions():
    config = dict()
    for action_name, class_Command_ in chain(['Day/Night Time', SunriseSunSetDayNight], iter_commands()):
        print(f'====== {action_name} Section ======')
        class_Command_.on_config_setup(config)
    return config


def edit_fields():
    with open(USER_CONFIG) as f:
        curr_config = yaml.safe_load(f)
    with open(USER_CONFIG + '.old', 'w') as f:
        yaml.safe_dump(curr_config, f)
    commands = [('Day/Night Time', SunriseSunSetDayNight)] + list(iter_commands())
    choices = [action_name for action_name, _ in commands] + ['Exit']
    choice = None
    while choice is None or choice != 'Exit':
        print('Select the field you want to edit or exit:')
        choice = pick(choices)
        if choice != 'Exit':
            action_f = commands[choices.index(choice)][1]
            action_f.on_config_setup(curr_config)
    print('Exiting...')
    return curr_config


def main():
    if not USER_CONFIG.exists():
        print('User config not exists, starting setup....')
        config = run_all_actions()
    else:
        print('Do you want to overwrite actual config or edit the current one?')
        choice = pick(['Overwrite', 'Edit'])
        if choice == 'Overwrite':
            config = run_all_actions()
        else:
            config = edit_fields()
    with open(USER_CONFIG, 'w') as f:
        yaml.safe_dump(config, f)
    print('Stored config into', str(USER_CONFIG))


if __name__ == "__main__":
    main()
