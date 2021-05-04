import os
from dataclasses import dataclass
from typing import Final

from daynight_theme.command import Command


def set_cmd_notification(title: str, body: str = None):
    cmd = f'notify-send "{title}"'
    if body:
        cmd += f' "{body}"'
    os.system(cmd)

@dataclass
class SendNotification(Command):

    day_value = 'Good day!'
    night_value = 'Good night!'

    def action(self, title: str, body: str = None):
        cmd = f'notify-send "{title}"'
        if body:
            cmd += f' "{body}"'
        os.system(cmd)


CMD_NOTIFICATION: Final[Command] = SendNotification()