from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @classmethod
    @abstractmethod
    def put_responce(self, address, responce):
        pass

    @classmethod
    @abstractmethod
    def save(self):
        pass
