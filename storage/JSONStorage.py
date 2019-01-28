from AbstractStorage import AbstractStorage
import json
from threading import RLock


class JSONStorage(AbstractStorage):

    def __init__(self, path):
        self.path = path
        self.respdict = dict()
        self.lock = RLock()

    def put_responce(self,  address,  responce):
        ip, port = address
        if ip not in self.respdict.keys():
            self.respdict[ip] = {"open": [], "close": []}
        self.respdict[ip]["open" if responce != 0 else "close"].append(port)

    def save(self):
        print("saving")
        with open(self.path, "w") as f:
            json.dump(self.respdict, f)
        self.respdict = {}
