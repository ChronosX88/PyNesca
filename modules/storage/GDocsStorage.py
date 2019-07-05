from core.prototypes.AbstractStorage import AbstractStorage
import json

class GDocsStorage(AbstractStorage):
    def __init__(self, path):
        self.path = path
        self.urls = dict()
    def put_responce(self, url:'url', status:'status'):
        if str(status) not in self.urls.keys():
            self.urls[str(status)] = []
        self.urls[str(status)].append(url)
    def save(self):
        print("saving")
        with open(self.path, "w") as f:
            json.dump(self.urls, f)
        self.urls = dict()
