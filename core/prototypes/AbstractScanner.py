from abc import abstractmethod
from core.prototypes.AbstractModuleClass import AbstractModuleClass

class AbstractScanner(AbstractModuleClass):
    '''By default the class is used by one thread to scan targets
    If it can manage many threads by itself set INDEPENDENT_THREAD_MANAGEMENT
    to "True"'''
    INDEPENDENT_THREAD_MANAGEMENT = False

    @abstractmethod
    def scan_address(self, address):
        '''This method should contain scanning process of given address. All
    items returned will be passed to AbstractStorage and ui'''
        pass
