import os
from typing import Final

from daynight_theme.command import Command


def set_cmd_notification(title: str, body: str = None):
    cmd = f'notify-send "{title}"'
    if body:
        cmd += f' "{body}"'
    os.system(cmd)

CMD_NOTIFICATION: Final[Command] = Command('Good day!', 'Good night!', set_cmd_notification)