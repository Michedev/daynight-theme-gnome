import os
from dataclasses import dataclass
from typing import Final, NoReturn

from rich.prompt import Confirm

from daynight_theme.command_register import register_command
from daynight_theme.commands.command import Command


def set_cmd_notification(title: str, body: str = None):
    cmd = f'notify-send "{title}"'
    if body:
        cmd += f' "{body}"'
    os.system(cmd)


@register_command(priority=2)
class SendNotification(Command):

    @staticmethod
    def is_runnable(config) -> bool:
        return config['daynight_notification']

    day_value = 'Good day!'
    night_value = 'Good night!'

    def action(self, title: str, body: str = None):
        cmd = f'notify-send "{title}"'
        if body:
            cmd += f' "{body}"'
        os.system(cmd)

    @staticmethod
    def on_config_setup(config) -> NoReturn:
        config['daynight_notification'] = \
            Confirm.ask('Do you want notification when switch day/night? [yes/no]')
