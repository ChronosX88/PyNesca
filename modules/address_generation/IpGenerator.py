from core.prototypes.AbstractAddressGenerator import AbstractAddressGenerator
from threading import RLock
import ipaddress
from types import GeneratorType

class IpGenerator(AbstractAddressGenerator):

    def set_parsed_fields(self, ips : 'ipv4_objects', ports : 'ports') -> None:
        self.ips = ips
        self.ports = ports
        self.lock = RLock()
    
    def get_next_port_number(self, previous_port):
        return (self.ports.index(previous_port) + 1) % len(self.ports)

    def get_next_address(self, previous_address : 'ipv4', previous_port :
    'port') -> {'ipv4', 'port'}:
        result = dict() 
        with self.lock:
            portnum = 0
            next_ip = None
            if previous_address:
                next_ip = previous_address
                port = previous_port
                portnum = self.get_next_port_number(port)
            if (portnum == 0):
                next_ip = None
                try:
                    while not next_ip:
                        if isinstance(self.ips[0], ipaddress.IPv4Address):
                            next_ip = self.ips.pop(0)
                        else:
                            if not isinstance(self.ips[0], GeneratorType):
                                self.ips[0] = self.ips[0].hosts()
                            try:
                                next_ip = next(self.ips[0])
                            except StopIteration:
                                self.ips.pop(0)
                except IndexError:
                    return None
            result["ipv4"] = next_ip
            result["port"] = self.ports[portnum]
            return result
    def get_all_addresses(self) -> {'ipv4_ranges', 'ports'}:
        result = dict()
        result['ipv4_ranges'] = self.ips
        result['ports'] = ports
        return result
