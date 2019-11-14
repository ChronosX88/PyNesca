from abc import abstractmethod
from core.prototypes.AbstractModuleClass import AbstractModuleClass


class AbstractParser(AbstractModuleClass):
    '''The class describes fields parsing mechanisms'''
    INPUT_FUNCTIONS = {}
    OUTPUT_FUNCTIONS = {"parse_fields"}
    @abstractmethod
    def parse_fields(self, args):
        '''In address field can be plased any text, describing address of
        scanning target.
        In port field only numbers, whitespaces, comma and '-' allowed.'''
        pass
