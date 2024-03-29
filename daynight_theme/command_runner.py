import asyncio
import time as t
from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import Literal, Optional, List

from daynight_theme.commands.command import Command
from daynight_theme.sunrise_sunset_api import sunrise_sunset_time


def diff_times_seconds(t1, t2):
    return timedelta(hours=t1.hour - t2.hour,
                     minutes=t1.minute - t2.minute,
                     seconds=t1.second - t2.second).total_seconds()


@dataclass
class CommandRunner:
    day_start: time
    day_end: time
    commands: List[Command]
    curr_dayt_zn: Optional[Literal['day_value', 'night_value']] = None

    def loop_forever(self):
        while True:
            daytime_zone = self.get_daytime_zome()
            if self.curr_dayt_zn is None or self.curr_dayt_zn != daytime_zone:
                self.exec_commands(daytime_zone)
                self.curr_dayt_zn = daytime_zone
            else:
                self.exec_commands_asap(daytime_zone)
            sleep_time = min([10 * 60, self.seconds_next_daytimezone()])
            t.sleep(sleep_time)  # 10 minutes

    def exec_commands(self, field: Literal['day_value', 'night_value']):
        for command in self.commands:
            field_value = getattr(command, field)  # command.day_value or command.night_value
            command.action(field_value)

    def exec_commands_asap(self, field: Literal['day_value', 'night_value']):
        for command in self.commands:
            if command.asap_update:
                dayzone_value = getattr(command, field)
                command.action(dayzone_value)

    def get_daytime_zome(self) -> Literal['day_value', 'night_value']:
        curr_time = datetime.now().time()
        if self.day_start <= curr_time < self.day_end:
            return 'day_value'
        else:
            return 'night_value'

    def seconds_next_daytimezone(self) -> float:
        curr_time = datetime.now().time()
        if self.day_start <= curr_time < self.day_end:
            return diff_times_seconds(self.day_end, curr_time)
        else:
            result = diff_times_seconds(self.day_start, curr_time)
            if result < 0:  # for cases like curr_time= 22:00 and day_start=06:00 of the next day
                result += 60 * 60 * 24
            return result


async def update_sunrise_sunset_everyday(cmd_runner):
    while True:
        await asyncio.sleep(24 * 60 * 60)  # wait one day
        sunset_sunrise = sunrise_sunset_time()
        print('Set sunrise to', sunset_sunrise.sunrise)
        print('Set sunset to', sunset_sunrise.sunset)
        cmd_runner.day_start = sunset_sunrise.sunrise
        cmd_runner.day_end = sunset_sunrise.sunset
