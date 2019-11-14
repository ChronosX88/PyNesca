from core.prototypes.AbstractStorage import AbstractStorage
import json
class GDocsStorage(AbstractStorage):
    def __init__(self, path:"path"):
        self.path = path
        self.urls = dict()
    def put_responce(self, url:'url', status:'status', title:'gdoc_title',
    info:'gdoc_info'):
        if str(status) not in self.urls.keys():
            self.urls[str(status)] = dict()
        print(int(status))
        url_object = dict()
        if status == 200:
            url_object = info
            url_object["title"] = title
        self.urls[str(status)][url] = url_object
    def save(self):
        print("saving")
        with open(self.path, "w") as f:
            json.dump(self.urls, f)
        self.urls = dict()
