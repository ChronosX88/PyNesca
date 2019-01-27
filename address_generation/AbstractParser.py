from abc import ABC, abstractmethod


class AbstractParser(ABC):

    @classmethod
    @abstractmethod
    def parse_address_field(self, field):
        pass

    @classmethod
    @abstractmethod
    def parse_port_field(self, field):
        pass
