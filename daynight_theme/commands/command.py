import os
from abc import ABC, abstractmethod, abstractproperty
from typing import NoReturn


class Command(ABC):

    def __init__(self, config: dict):
        self.config = config

    @property
    @abstractmethod
    def day_value(self) -> str:
        pass

    @property
    @abstractmethod
    def night_value(self) -> str:
        pass

    asap_update: bool = False

    @abstractmethod
    def action(self, value: str):
        pass

    @staticmethod
    @abstractmethod
    def is_runnable(config) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def on_config_setup(config) -> NoReturn:
        pass
