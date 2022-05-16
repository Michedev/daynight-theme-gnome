from dataclasses import dataclass, field
from datetime import datetime, time
from dateutil.parser import parse
from typing import Union, Optional
import requests
from tenacity import retry, wait_exponential

FLORENCE_LAT = 43.7799528
FLORENCE_LONG = 11.2059486

Number = Union[int, float]


def to_seconds(v: time) -> int:
    return v.hour * 3600 + v.minute * 60 + v.second


@dataclass
class SunriseSunsetData:
    sunrise: time = None
    sunset: time = None

    def __post_init__(self):
        self.delta_sunset_sunrise_seconds: int = self.diff_times_seconds(self.sunset, self.sunrise)
        self.delta_sunrise_sunset_seconds: int = self.diff_times_seconds(self.sunrise, self.sunset)

    def diff_times_seconds(self, time_a, time_b):
        diff = to_seconds(time_a) - to_seconds(time_b)
        if diff < 0:
            diff = 24 * 60 * 60 + diff
        return diff

    def diff_sunrise_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunrise
        """

        if currtime is None:
            currtime = datetime.now().time()
        return self.diff_times_seconds(currtime, self.sunrise)

    def diff_sunset_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunset
        """
        if currtime is None:
            currtime = datetime.now().time()
        return self.diff_times_seconds(currtime, self.sunset)

    def sunrise_diffseconds(self, currtime: Optional[time] = None):
        """
        :return: sunrise - currtime
        """

        if currtime is None:
            currtime = datetime.now().time()
        return self.diff_times_seconds(self.sunrise, currtime)

    def sunset_diff_seconds(self, currtime: Optional[time] = None):
        """
        :return: currtime - sunset
        """
        if currtime is None:
            currtime = datetime.now().time()
        return self.diff_times_seconds(self.sunset, currtime)


def sunset_sunrise_url(lat: Number, long: Number):
    return f'http://api.sunrise-sunset.org/json?lat={lat}&lng={long}'


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def sunrise_sunset_time(lat=FLORENCE_LAT, long=FLORENCE_LONG) -> SunriseSunsetData:
    url = sunset_sunrise_url(lat, long)
    result = requests.get(url).json()
    if result['status'].lower() == 'ok':
        sunrise = parse(result['results']['nautical_twilight_begin']).time()
        sunset = parse(result['results']['nautical_twilight_end']).time()
        return SunriseSunsetData(sunrise, sunset)
    else:
        raise ValueError("request status is not ok")
