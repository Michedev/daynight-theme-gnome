import os
from abc import ABC, abstractmethod


class Command(ABC):
    day_value: str
    night_value: str

    @abstractmethod
    def action(self, value: str):
        pass
