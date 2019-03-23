from AbstractAddressGenerator import AbstractAddressGenerator
from threading import RLock
from core.communication.CommunicationDictionary import CommunicationDictionary

class IpGenerator(AbstractAddressGenerator):

    def __init__(self, ip_generator, ports, convert_table):
        self.convert_table = convert_table
        self.ip_generator = ip_generator
        self.ports = ports
        self.lock = RLock()

    def get_next_port_number(self, previous_port):
        return (self.ports.index(previous_port) + 1) % len(self.ports)

    def get_next_address(self, previous_address):
        result = CommunicationDictionary(self.convert_table)
        with self.lock:
            portnum = 0
            next_ip = None
            if previous_address:
                next_ip = previous_address["ipv4"]
                port = previous_address["port"]
                portnum = self.get_next_port_number(port)
            if (portnum == 0):
                try:
                    next_ip = next(self.ip_generator)
                except StopIteration:
                    return None
            result["ipv4"] = next_ip
            result["port"] = self.ports[portnum]
            return result
