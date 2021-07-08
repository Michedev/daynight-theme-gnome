import os
from abc import ABC, abstractmethod


class Command(ABC):
    day_value: str
    night_value: str
    asap_update: bool = False

    @abstractmethod
    def action(self, value: str):
        pass
