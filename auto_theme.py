from datetime import datetime, time, timedelta
from dateutil.parser import parse
from path import Path
import json
import time
from fire import Fire
import os


USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'auto-gnome-theme.json'

def run_cmd(f):
    def wrapper(themename):
        cmd = f(themename)
        os.system(cmd)
    return wrapper

@run_cmd
def set_shell_theme_cmd(theme):
    return f'gsettings set org.gnome.shell.extensions.user-theme name "{theme}"'

@run_cmd
def set_theme_cmd(theme: str):
    return f'gsettings set org.gnome.desktop.interface gtk-theme "{theme}"'

def set_theme(day_theme: str, night_theme: str, day_start: time, day_end: time):
    curr_time = datetime.now()
    if day_start <= curr_time < day_end:
        set_theme_cmd(day_theme)
    else:
        set_theme_cmd(night_theme)

def loop(day_theme: str, night_theme: str, day_start: time, day_end: time):
    while True:
        set_theme(day_theme, night_theme, day_start, day_end)
        now = datetime.now()
        if now > day_start:
            sleeptime = day_end - now
        elif now > day_end:
            sleeptime = day_start - now + timedelta(seconds=24*60*60)
        else:
            sleeptime = day_start - now
        time.sleep((sleeptime.seconds+1) * 1000)

def parse_input(day_theme: str, night_theme: str, day_start: str, day_end: str):
    if day_theme is None:
        day_theme = 'Adwaita'
    if night_theme is None:
        night_theme = 'Adwaita-dark'
    if USER_CONFIG.exists():
        with open(USER_CONFIG) as f:
            old_config = json.load(f)
        if 'day_theme' in old_config: day_theme = old_config['day_theme']
        if 'night_theme' in old_config: night_theme = old_config['night_theme']
        if 'day_start' in old_config: day_start = old_config['day_start']
        if 'day_end' in old_config: day_end = old_config['day_end']
        del old_config
    with open(USER_CONFIG, 'w') as f:
        config = locals()
        del config['f']
        json.dump(config, f)
    del f, config
    day_start, day_end = parse(day_start), parse(day_end)
    return locals()

def main(day_theme=None, night_theme=None, day_start='06:00', day_end='18:00'):
    config = parse_input(**locals())
    loop(**config)
    
if __name__ == "__main__":
    Fire(main)