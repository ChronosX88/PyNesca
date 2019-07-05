from abc import abstractmethod
from core.prototypes.AbstractModuleClass import AbstractModuleClass

class AbstractStorage(AbstractModuleClass):

    @abstractmethod
    def put_responce(self, address, responce):
        pass

    @abstractmethod
    def save(self):
        pass
