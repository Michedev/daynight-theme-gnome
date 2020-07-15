from path import Path
import os
from random import shuffle
import time
import json
from fire import Fire

USER_CONFIG = Path(os.environ['HOME']) / '.config' / 'auto-background.json'

def run_cmd(f):
    def wrapper(imgpath):
        cmd = f(imgpath)
        os.system(cmd)
    return wrapper

@run_cmd
def cmd_set_background_gnome(imgpath):
    return f"gsettings set org.gnome.desktop.background picture-uri {imgpath.abspath()}"

def loop(folder, sleeptime):
    while True:
        images = list(folder.files())
        shuffle(images)
        for imgpath in images:
            cmd_set_background_gnome(imgpath)
            time.sleep(sleeptime)


def main(folder=None, sleeptime=None):
    """
    Give priority to input function, if not available read values stored into ~/.config/auto-background.json;
    if the file is not available then set some default parameters (folder = ~/Pictures/Wallpaper - sleeptime = 10 minutes)
    :param folder: folder of background images (default ~/Pictures/Wallpaper)
    :param sleeptime: background switch time in millisecond (default 10 * 60 * 1000 i.e. 10 minutes)
    """
    any_none = folder is None or sleeptime is None
    if any_none and USER_CONFIG.exists():
        with open(USER_CONFIG) as f:
            config = json.load(f)
        if folder is None:
            folder = config['folder']
        if sleeptime is None:
            sleeptime = config['sleeptime'] 
    elif any_none:
        if folder is None:
            folder = Path(os.environ['HOME']) / 'Pictures' / 'Wallpaper'
        if sleeptime is None:
            sleeptime = 10 * 60 * 1000 #i.e. 10 minutes
    with open(USER_CONFIG, 'w') as f:
        json.dump({'folder': folder, 'sleeptime': sleeptime}, f)
    loop(folder, sleeptime)
    

if __name__ == "__main__":
    Fire(main)
