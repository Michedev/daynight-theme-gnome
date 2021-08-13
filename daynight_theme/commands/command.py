import os
from abc import ABC, abstractmethod, abstractproperty


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
    def can_add_to_registry(config) -> bool:
        pass
