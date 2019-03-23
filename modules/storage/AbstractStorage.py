from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @abstractmethod
    def put_responce(self, address, responce):
        pass

    @abstractmethod
    def save(self):
        pass
