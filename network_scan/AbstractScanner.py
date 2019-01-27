from abc import ABC, abstractmethod


class AbstractScanner(ABC):

    @classmethod
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def scan_address(self, address):
        pass
