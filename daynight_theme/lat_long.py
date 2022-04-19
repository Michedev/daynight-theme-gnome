import subprocess
import json
import urllib
from typing import Tuple
from collections import namedtuple

Location = namedtuple('Location', ['lat', 'long'])

def get_external_ip_address() -> str:
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip


def get_lat_long_by_ip_address(ip_address: str) -> Location:
    json_reply = subprocess.run(f'curl ipinfo.io/{ip_address}'.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
    lat, long = json.loads(json_reply)['loc'].split(',')
    lat, long = float(lat), float(long)
    return Location(lat, long)


def get_lat_long() -> Location:
    return get_lat_long_by_ip_address(get_external_ip_address())
