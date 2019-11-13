import socket
from core.prototypes.AbstractScanner import AbstractScanner

class CoreModel(AbstractScanner):
    def __init__(self, timeout:"timeout"):
        self.defSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.defSocket.settimeout(int(timeout))

    def scan_address(self, host:'ipv4_str', port:'port') -> {'scan_result'}:
        result = dict()
        if not host: raise Exception
        result["scan_result"] = self.defSocket.connect_ex((host, port))
        self.defSocket.close()
        return result
