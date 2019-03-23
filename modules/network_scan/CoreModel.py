import socket
from AbstractScanner import AbstractScanner
from core.communication.CommunicationDictionary import CommunicationDictionary

class CoreModel(AbstractScanner):
    def __init__(self, timeout):
        self.defSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.defSocket.settimeout(int(timeout))

    def scan_address(self, address: CommunicationDictionary) -> CommunicationDictionary:
        host = address["str"]
        port = address["port"]
        if not host: raise Exception
        result = self.defSocket.connect_ex((host, port))
        self.defSocket.close()
        self.defSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return result
