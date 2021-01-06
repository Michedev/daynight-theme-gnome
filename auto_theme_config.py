from pick import pick
from path import Path
from datetime import datetime
import yaml
import os
import re

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'daynight-gnome-theming.yaml'


def parse_time(msg, default_value):
    time_regex = '^$|([0-9]{1,2}:[0-9]{1,2})'
    matcher = re.compile(time_regex)
    while not matcher.match(time := input(msg)):
        print('wrong input, it should be on the form HH:MM')
    if not time:
        time = default_value

    time = datetime.strptime(time, "%H:%M").time()
    return time


def main():
    theme_folder = Path(os.environ['HOME']) / '.themes'
    day_theme_msg = 'Pick Gnome theme chosen during the day'
    night_theme_msg = 'Pick Gnome theme chosen during the night'
    themes_list = [d.basename() for d in theme_folder.dirs()]
    day_theme, day_index = pick(themes_list, day_theme_msg)
    themes_list.remove(day_theme)
    night_theme, night_index = pick(themes_list, night_theme_msg)

    time_start = parse_time('Insert time in the form HH:MM when the day theme starts: [default 06:00] ', '06:00')
    time_end = parse_time('Insert time in the form HH:MM when the day theme ends: [default 18:00] ', '18:00')

    config = {'day_theme': day_theme, 'night_theme': night_theme,
              'day_start': time_start.strftime("%H:%M"),
              'day_end': time_end.strftime("%H:%M")}
    with open(USER_CONFIG, 'w') as f:
        yaml.safe_dump(config, f, allow_nan=False)


if __name__ == "__main__":
    main()
