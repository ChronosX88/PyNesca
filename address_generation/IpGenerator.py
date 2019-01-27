from AbstractAddressGenerator import AbstractAddressGenerator
from threading import RLock

class IpGenerator(AbstractAddressGenerator):

    def __init__(self, address_generator, ports):
        self.address_generator = address_generator
        self.ports = ports
        self.portnum = -1
        self.lock = RLock()

    def get_next_address(self, previous_address):
        with self.lock:
            self.portnum = (self.portnum + 1) % len(self.ports)
            try:
                return (str(next(self.address_generator)), self.ports[self.portnum])
            except StopIteration:
                return None
