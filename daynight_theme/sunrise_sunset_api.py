import asyncio
from dataclasses import dataclass
from datetime import datetime, time
from dateutil.parser import parse
from typing import Tuple, Union, Optional
import requests
from tenacity import retry, wait_exponential

FLORENCE_LAT = 43.7799528
FLORENCE_LONG = 11.2059486

Number = Union[int, float]


@dataclass
class SunriseSunsetData:
    sunrise: time
    sunset: time

    def __post_init__(self):
        self.delta_sunset_sunrise_seconds: int = self.sunset.second - self.sunrise.second
        self.delta_sunrise_sunset_seconds: int = 24 * 60 * 60 - (self.sunrise.second - self.sunset.second)

    def _diff_times_seconds(self, time_a, time_b):
        diff = time_a.second - time_b.second
        if diff < 0:
            diff = 24 * 60 * 60 - diff
        return diff

    def diff_sunrise_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunrise
        """

        if currtime is None:
            currtime = datetime.now().time()
        return self._diff_times_seconds(currtime, self.sunrise)

    def diff_sunset_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunset
        """
        if currtime is None:
            currtime = datetime.now().time()
        return self._diff_times_seconds(currtime, self.sunset)

    def sunrise_diffseconds(self, currtime: Optional[time] = None):
        """
        :return: sunrise - currtime
        """

        if currtime is None:
            currtime = datetime.now().time()
        return self._diff_times_seconds(self.sunrise, currtime)

    def sunset_diff_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunset
        """
        if currtime is None:
            currtime = datetime.now().time()
        return self._diff_times_seconds(self.sunset, currtime)


def sunset_sunrise_url(lat: Number, long: Number):
    return f'https://api.sunrise-sunset.org/json?lat={lat}&lng={long}'


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def sunrise_sunset_time(lat=FLORENCE_LAT, long=FLORENCE_LONG) -> SunriseSunsetData:
    url = sunset_sunrise_url(lat, long)
    result = requests.get(url).json()
    if result['status'].lower() == 'ok':
        sunrise = parse(result['results']['sunrise']).time()
        sunset = parse(result['results']['sunset']).time()
        return SunriseSunsetData(sunrise, sunset)
    else:
        raise ValueError("request status is not ok")


async def set_sunrise_sunset_everyday(command_runner):
    while True:
        sunset_sunrise = sunrise_sunset_time()
        print('Set sunrise to', sunset_sunrise.sunrise)
        print('Set sunset to', sunset_sunrise.sunset)
        command_runner.day_start = sunset_sunrise.sunrise
        command_runner.day_end = sunset_sunrise.sunset
        await asyncio.sleep(24 * 60 * 60)  # wait one day
