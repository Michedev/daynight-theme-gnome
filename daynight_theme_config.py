from collections import Iterable

from path import Path
from datetime import datetime
import yaml
import os
from rich.prompt import IntPrompt, Confirm
import re

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'
ROOT_THEMES = Path(os.environ['HOME']) / '.themes'

def parse_time(msg, default_value):
    time_regex = '^$|([0-9]{1,2}:[0-9]{1,2})'
    matcher = re.compile(time_regex)
    while not matcher.match(time := input(msg)):
        print('wrong input, it should be on the form HH:MM')
    if not time:
        time = default_value

    time = datetime.strptime(time, "%H:%M").time()
    return time


def pick(choices: list):
    msg = ""
    for i, v in enumerate(choices):
        msg += f'{i + 1}) {v}\n'
    int_choices = [str(x) for x in range(1, len(choices) + 1)]
    picked = IntPrompt.ask(msg, choices=int_choices, show_choices=False)
    return choices[picked-1]


def gnome_shell_themes() -> list:
    root = Path(os.environ['HOME']) / '.themes'
    return [folder.basename() for folder in root.dirs() if (folder / 'gnome-shell') in folder.dirs()]


def main():
    day_theme, night_theme = prompt_gtk_theme()
    shell_themes = prompt_gnome_shell_themes()
    daynight_pycharm = prompt_pycharm()
    time_start = parse_time('Insert time in the form HH:MM when the day theme starts: [default 06:00] ', '06:00')
    time_end = parse_time('Insert time in the form HH:MM when the day theme ends: [default 18:00] ', '18:00')

    config = {'day_theme': day_theme, 'night_theme': night_theme,
              'day_start': time_start.strftime("%H:%M"),
              'day_end': time_end.strftime("%H:%M"),
              'pycharm': daynight_pycharm}
    if shell_themes:
        config['day_shell_theme'] = shell_themes[0]
        config['night_shell_theme'] = shell_themes[1]
    with open(USER_CONFIG, 'w') as f:
        yaml.safe_dump(config, f)


def prompt_gnome_shell_themes():
    add_shell_theme = Confirm.ask("Do you want to enter gnome shell theme too? [yes/no]")
    if add_shell_theme:
        day_theme_msg = 'Pick Gnome shell theme chosen during the day'
        night_theme_msg = 'Pick Gnome shell theme chosen during the night'
        themes_list = gnome_shell_themes()
        print(day_theme_msg)
        day_shell_theme = pick(themes_list)
        themes_list.remove(day_shell_theme)
        print(night_theme_msg)
        night_shell_theme = pick(themes_list)
        return str(day_shell_theme), str(night_shell_theme)
    return None


def prompt_gtk_theme():
    themes_list = gtk_themes()
    day_theme_msg = 'Pick Gnome theme chosen during the day'
    night_theme_msg = 'Pick Gnome theme chosen during the night'
    print(day_theme_msg)
    day_theme = pick(themes_list)
    themes_list.remove(day_theme)
    print(night_theme_msg)
    night_theme = pick(themes_list)
    return str(day_theme), str(night_theme)

def prompt_pycharm():
    prompt = Confirm.ask("Do you want day/night switch for pycharm? [yes/no]")
    return str(prompt)

def gtk_themes():
    theme_folder = Path(os.environ['HOME']) / '.themes'
    themes_list = [d.basename() for d in theme_folder.dirs()]
    return themes_list


if __name__ == "__main__":
    main()
