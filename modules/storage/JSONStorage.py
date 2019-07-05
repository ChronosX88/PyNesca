from core.prototypes.AbstractStorage import AbstractStorage
import json
from threading import RLock

class JSONStorage(AbstractStorage):

    def __init__(self, path):
        self.path = path
        self.respdict = dict()
        self.lock = RLock()

    def put_responce(self, ip:'ipv4_str', port:'port', scan_result:'scan_result'):
        if ip not in self.respdict.keys():
            self.respdict[ip] = {"open": [], "close": []}
        self.respdict[ip]["open" if scan_result == 0
        else "close"].append(port)

    def save(self):
        print("saving")
        with open(self.path, "w") as f:
            json.dump(self.respdict, f)
        self.respdict = {}
