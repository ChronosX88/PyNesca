from abc import abstractmethod, ABC
from core.communication import CommunicationDictionary


class AbstractAddressGenerator(ABC):
    '''The class describes addess generation mechanism.
    In __init__ method it should get results of parsing fields
    and then it returns addresses.'''
    @abstractmethod
    def get_next_address(self, previous_address, **kwargs) -> CommunicationDictionary:
        '''Address - an only, indivisible object, that describes single scan
        target address. This method should return next address to scan based on
        previous scanned address and result of scanning previous address, that
        can be placed in kwargs.'''
        pass
