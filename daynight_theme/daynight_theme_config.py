import os
import re
from datetime import datetime

import yaml
from path import Path
from rich.prompt import IntPrompt, Confirm, FloatPrompt

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


def gnome_shell_themes() -> list:
    root = Path(os.environ['HOME']) / '.themes'
    return [folder.basename() for folder in root.dirs() if (folder / 'gnome-shell') in folder.dirs()]


def prompt_api_sunrise_sunfall():
    prompt = Confirm.ask('Do you want to pull from APIs automatically sunrise and sunfall time? [yes/no]')
    if prompt:
        lat = FloatPrompt.ask('Please insert the latitude coordinate of your location (need to call APIs)')
        long = FloatPrompt.ask('Please insert the longitude coordinate of your location (need to call APIs)')
        return prompt, lat, long
    return prompt, None, None


def ask_notification():
    return Confirm.ask('Do you want notification when switch day/night? [yes/no]')


def ask_unite_button():
    if not UNITE_PATH.exists():
        print('Warning: Unite extension not found at path', str(UNITE_PATH))
        return False, None
    ans = Confirm.ask('Do you want to switch day night unite buttons? [yes/no]')
    if ans:
        pick_ans = Confirm.ask('Do you want to choose button theme? [default is united-dark/united-light]')
        if pick_ans:
            theme_list = [x.basename for x in (UNITE_PATH / 'themes').dirs()]
            day_theme = pick(theme_list, 'Select day button theme:')
            print()
            theme_list.remove(day_theme)
            night_theme = pick(theme_list, 'Select night button theme:')
        else:
            day_theme = 'united-dark'
            night_theme = 'united-light'
        return ans, (day_theme, night_theme)
    else:
        return ans, None


def gtk_theme_action(config):
    day_theme, night_theme = prompt_gtk_theme()
    config['day_theme'] = day_theme
    config['night_theme'] = night_theme


def shell_theme_action(config):
    if shell_themes := prompt_gnome_shell_themes():
        config['day_shell_theme'] = shell_themes[0]
        config['night_shell_theme'] = shell_themes[1]


def bitday_action(config):
    config['bitday_background'] = prompt_bitday()


def pycharm_action(config):
    config['pycharm'] = prompt_pycharm()


def daynight_action(config):
    use_api_sunrise_sunfall, lat, long = prompt_api_sunrise_sunfall()
    if use_api_sunrise_sunfall:
        config['use_api_sunrise_sunfall'] = use_api_sunrise_sunfall
        config['api_latitude'] = lat
        config['api_longitude'] = long
    if not use_api_sunrise_sunfall:
        time_start = parse_time('Insert time in the form HH:MM when the day theme starts: [default 06:00] ', '06:00')
        time_end = parse_time('Insert time in the form HH:MM when the day theme ends: [default 18:00] ', '18:00')
        config['day_start'] = time_start.strftime("%H:%M")
        config['day_end'] = time_end.strftime("%H:%M")


def notification_action(config):
    config['daynight_notification'] = ask_notification()


def unite_button_action(config):
    use_unite_btn, themes = ask_unite_button()
    config['unite_button'] = use_unite_btn
    if use_unite_btn:
        config['unite_daybutton'] = themes[0]
        config['unite_nightbutton'] = themes[1]


def prompt_gnome_shell_themes():
    add_shell_theme = Confirm.ask("Do you want to enter gnome shell theme too? [yes/no]")
    if add_shell_theme:
        day_theme_msg = 'Pick Gnome shell theme chosen during the day'
        night_theme_msg = 'Pick Gnome shell theme chosen during the night'
        themes_list = gnome_shell_themes()
        day_shell_theme = pick(themes_list, day_theme_msg)
        themes_list.remove(day_shell_theme)
        night_shell_theme = pick(themes_list, night_theme_msg)
        return str(day_shell_theme), str(night_shell_theme)
    return None


ACTIONS = [(name.replace('_action', '').replace('_', ' ').capitalize(), v) for name, v in locals().items() if
           name.endswith('_action') and hasattr(v, '__call__')]

ACTIONS = dict(ACTIONS)


def prompt_gtk_theme():
    themes_list = gtk_themes()
    day_theme_msg = 'Pick Gnome theme chosen during the day'
    night_theme_msg = 'Pick Gnome theme chosen during the night'
    print()
    day_theme = pick(themes_list, day_theme_msg)
    themes_list.remove(day_theme)
    print()
    night_theme = pick(themes_list, night_theme_msg)
    return str(day_theme), str(night_theme)


def prompt_pycharm():
    prompt = Confirm.ask("Do you want day/night switch for pycharm? [yes/no]")
    return prompt


def prompt_bitday():
    prompt = Confirm.ask('Do you want bitday background? [yes/no]')
    if prompt:
        _download_bitday_images()
    return prompt


def _download_bitday_images():
    try:
        from mega import Mega
    except ImportError:
        os.system('pip install --user mega.py')
        from mega import Mega
    import zipfile
    os.chdir(Path(os.environ['HOME']) / 'Pictures')
    instance = Mega()
    instance.login_anonymous()
    instance.download_url('https://mega.nz/file/L55EHRoJ#kqbzKJUlQtIiZj4QZFl5Gcp7ebu_l2CR-pdL56gthOM')
    dst_folder = Path('bitday')
    if dst_folder.exists():
        dst_folder.rmtree()
    dst_folder.mkdir()
    with zipfile.ZipFile('./BitDay-2-1920x1080.zip', 'r') as f:
        f.extractall(dst_folder)
    (dst_folder / '__MACOSX').rmtree()
    images_folder: Path = dst_folder / '1920x1080'
    for img in images_folder.files('*.png'):
        img.move(dst_folder)
    images_folder.rmtree()
    print('Put bitday images into', dst_folder.abspath())


def gtk_themes():
    theme_folder = Path(os.environ['HOME']) / '.themes'
    themes_list = [d.basename() for d in theme_folder.dirs()]
    return themes_list


def run_all_actions():
    config = dict()
    for action_name, action_f in ACTIONS.items():
        print(f'====== {action_name} Section ======')
        action_f(config)
    return config


def edit_fields():
    with open(USER_CONFIG) as f:
        curr_config = yaml.safe_load(f)
    with open(USER_CONFIG + '.old', 'w') as f:
        yaml.safe_dump(curr_config, f)
    choices = [action_name for action_name in ACTIONS] + ['Exit']
    choice = None
    while choice is None or choice != 'Exit':
        print('Select the field you want to edit or exit:')
        choice = pick(choices)
        if choice != 'Exit':
            action_f = ACTIONS[choice]
            action_f(curr_config)
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
