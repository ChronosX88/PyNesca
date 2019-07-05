from core.prototypes.AbstractAddressGenerator import AbstractAddressGenerator
from core.communication.CommunicationDictionary import CommunicationDictionary

class PlugAddressGenerator(AbstractAddressGenerator):

    def __init__(self, all_addresses, ports, convert_table):
        self.res = CommunicationDictionary(convert_table) 
        self.res["address_list"] = all_addresses
        self.res["ports"] = ports
    def get_next_address(self, previous_address):
        res = self.res
        self.res = None
        return res
