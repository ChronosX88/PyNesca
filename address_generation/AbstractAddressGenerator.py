from abc import abstractmethod, ABC


class AbstractAddressGenerator(ABC):

    @classmethod
    @abstractmethod
    def get_next_address(self, previous_address, **kwargs):
        pass
