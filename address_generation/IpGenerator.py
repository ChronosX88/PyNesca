from AbstractAddressGenerator import AbstractAddressGenerator
from threading import RLock


class IpGenerator(AbstractAddressGenerator):

    def __init__(self, ip_generator, ports):
        self.ip_generator = ip_generator
        self.ports = ports
        self.lock = RLock()

    def get_next_port_number(self, previous_port):
        return (self.ports.index(previous_port) + 1) % len(self.ports)

    def get_next_address(self, previous_address):
        with self.lock:
            portnum = 0
            next_ip = None
            if previous_address:
                next_ip, port = previous_address
                portnum = self.get_next_port_number(port)
            if (portnum == 0):
                try:
                    next_ip = str(next(self.ip_generator))
                except StopIteration:
                    return None
            result = (next_ip, self.ports[portnum])
            return result
