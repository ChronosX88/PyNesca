from core.prototypes.AbstractScanner import AbstractScanner
import requests

class URLScanner(AbstractScanner):

    def __init__(self, timeout):
       pass 

    def scan_address(self, url:"url") -> {"response"}:
        return {'response':requests.get(url)}
