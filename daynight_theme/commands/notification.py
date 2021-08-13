import os
from dataclasses import dataclass
from typing import Final

from daynight_theme.commands.command import Command


def set_cmd_notification(title: str, body: str = None):
    cmd = f'notify-send "{title}"'
    if body:
        cmd += f' "{body}"'
    os.system(cmd)


class SendNotification(Command):

    @staticmethod
    def can_add_to_registry(config) -> bool:
        return config['daynight_notification']

    day_value = 'Good day!'
    night_value = 'Good night!'

    def action(self, title: str, body: str = None):
        cmd = f'notify-send "{title}"'
        if body:
            cmd += f' "{body}"'
        os.system(cmd)


