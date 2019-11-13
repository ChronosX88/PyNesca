from abc import abstractmethod
from core.prototypes.AbstractModuleClass import AbstractModuleClass

class AbstractAddressGenerator(AbstractModuleClass):
    '''The class describes addess generation mechanism.'''
    INPUT_FUNCTIONS = {"set_parsed_fields", "get_next_address"}
    OUTPUT_FUNCTIONS = {"get_next_address", "get_all_addresses"}
    @abstractmethod
    def set_parsed_fields(self):
       '''This method is called after generator initialization. It is used to
       store parsing results for futher address generation''' 
       pass
    @abstractmethod
    def get_next_address(self, previous_address, scan_result):
        '''Address - an only, indivisible object, that describes single scan
        target address. This method should return next address to scan based on
        previous scanned address and result of scanning previous address, that
        can be placed in kwargs.
        Scan results is results of scan got from parser'''
        pass

    @abstractmethod
    def get_all_addresses(self):
        '''This method is used to return all addresses (ip ranges, url
        patterns, etc) at one time to scnners with self thread management'''
        pass
