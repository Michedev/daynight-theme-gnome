import os
import time as t
from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import Iterable, Literal

from daynight_theme.command import Command


def diff_times_seconds(t1, t2):
    return timedelta(hours=t1.hour - t2.hour,
                     minutes=t1.minute - t2.minute,
                     seconds=t1.second - t2.second).total_seconds()

@dataclass
class CommandRunner:

    commands: Iterable[Command]
    day_start: time
    day_end: time

    def loop_forever(self):
        while True:
            daytime_zone = self.get_daytime_zome()
            self.exec_commands(daytime_zone)
            sleep_time = min([10 * 60, self.get_remaining_time_seconds()])
            t.sleep(sleep_time)  # 10 minutes

    def exec_commands(self, field: Literal['day_value', 'night_value']):
        for command in self.commands:
            field_value = getattr(command, field)
            command.action(field_value)

    def get_daytime_zome(self) -> Literal['day_value', 'night_value']:
        curr_time = datetime.now().time()
        if self.day_start <= curr_time < self.day_end:
            return 'day_value'
        else:
            return 'night_value'

    def get_remaining_time_seconds(self) -> int:
        curr_time = datetime.now().time()
        if self.day_start <= curr_time < self.day_end:
            return diff_times_seconds(self.day_end, curr_time)
        else:
            result = diff_times_seconds(self.day_start, curr_time)
            if result < 0:  # for cases like curr_time= 22:00 and day_start=06:00 of the next day
                result += 60 * 60 * 24
            return result