from abc import ABC, abstractmethod


class AbstractParser(ABC):
    '''The class describes fields parsing mechanisms'''

    @abstractmethod
    def parse_address_field(self, field):
        '''In address field can be plased any text, describing address of
        scanning target'''
        pass

    @abstractmethod
    def parse_port_field(self, field):
        '''In port field only numbers, whitespaces, comma and '-' allowed'''
        pass
