import os
import re
from datetime import datetime

import yaml
from path import Path
from rich.prompt import IntPrompt

from daynight_theme.command_register import iter_commands

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
ROOT_THEMES = Path(os.environ['HOME']) / '.themes'
UNITE_PATH = Path(os.environ['HOME']) / '.local' / 'share' / 'gnome-shell' / 'extensions' / 'unite@hardpixel.eu'


def parse_time(msg, default_value):
    time_regex = '^$|([0-9]{1,2}:[0-9]{1,2})'
    matcher = re.compile(time_regex)
    while not matcher.match(time := input(msg)):
        print('wrong input, it should be on the form HH:MM')
    if not time:
        time = default_value

    time = datetime.strptime(time, "%H:%M").time()
    return time


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


def run_all_actions():
    config = dict()
    for action_name, class_Command_ in iter_commands():
        print(f'====== {action_name} Section ======')
        class_Command_.on_config_setup(config)
    return config


def edit_fields():
    with open(USER_CONFIG) as f:
        curr_config = yaml.safe_load(f)
    with open(USER_CONFIG + '.old', 'w') as f:
        yaml.safe_dump(curr_config, f)
    commands = list(iter_commands())
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
