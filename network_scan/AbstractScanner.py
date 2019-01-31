from abc import ABC, abstractmethod


class AbstractScanner(ABC):
    '''The class is used by one thread to scan targets'''

    @classmethod
    @abstractmethod
    def __init__(self, **kwargs):
        '''In this method you can init some
        reusable resources needed for scan'''
        pass

    @classmethod
    @abstractmethod
    def scan_address(self, address):
        '''This method should contain scanning process of given address. All
    items returned will be passed to AbstractStorage and ui'''
        pass
