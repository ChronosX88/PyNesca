from core.prototypes.AbstractStorage import AbstractStorage
import json
from threading import RLock

class JSONStorage(AbstractStorage):

    def __init__(self, path:"path", scheme:"json_scheme"):
        self.path = path
        self.scheme = scheme
        self.needed_keys = set()
        if type(scheme) == dict:
            left_nodes = []
            self.needed_keys = self.needed_keys.union(set(
                filter(JSONStorage.is_needed_key,scheme.keys())))
            left_nodes.extend(scheme.values())
            for node in left_nodes:
                if type(node) == str and JSONStorage.is_needed_key(node): 
                    self.needed_keys.add(node)
                elif type(node) == set or type(node) == list:
                    left_nodes.extend(list(node))
                    #self.needed_keys = self.needed_keys.union(set(
                        #filter(JSONStorage.is_needed_key, node)))
                elif type(node) == dict:
                    self.needed_keys = self.needed_keys.union(
                            set(filter(JSONStorage.is_needed_key,
                        node.keys())))
                    left_nodes.extend(node.values())
        elif type(scheme) == set or type(scheme) == list:
            self.needed_keys = set(
                    filter(JSONStorage.is_needed_key, scheme.copy()))
        elif type(scheme) == str and JSONStorage.is_needed_key(scheme):
            self.needed_keys.add(scheme)
        self.respdict = type(scheme)() 
        self.needed_keys = list(self.needed_keys)
        setattr(self.put_responce.__func__, "__annotations__", {str(i):arg for
        i, arg in enumerate(self.needed_keys)})
        self.lock = RLock()
        
    '''def put_responce(self, ip:'ipv4_str', port:'port', scan_result:'scan_result'):
        if ip not in self.respdict.keys():
            self.respdict[ip] = {"open": [], "close": []}
        self.respdict[ip]["open" if scan_result == 0
        else "close"].append(port)'''
    #Все ключи, начинающиеся с "@", считаются значениями и не декодируются.
    @staticmethod
    def is_needed_key(string):
        return not string.startswith("@")
    @staticmethod
    def get_element_name(key, named_args):
        return key[1:] if not JSONStorage.is_needed_key(key) else named_args[key]
    @staticmethod
    def get_node_adder(node, key = None):
        adder = None
        if key == None:
            adder = node.append if type(node) == list else node.add
        elif type(key) == str:
            def result(x):
                node[key] = x
            adder = result
        return adder
    @staticmethod
    def process_scheme(scheme, current_level, named_args):
       print("processing scheme", scheme)
       if type(scheme) == str:
                JSONStorage.get_node_adder(current_level)(JSONStorage.get_element_name(scheme, named_args))
       elif type(scheme) == set or type(scheme) == list:
           for el in scheme:
               if type(el) == str:
                   JSONStorage.process_scheme(el, current_level, named_args)
               elif type(el) == dict:
                    current_level.append(dict())
                    JSONStorage.process_scheme(el, current_level[-1], named_args)
       elif type(scheme) == dict:
            for key, value in scheme.items():
                reversed_key = JSONStorage.get_element_name(key, named_args) 
                if type(value) == str:
                    print(value, named_args)
                    JSONStorage.get_node_adder(current_level,
                            reversed_key)(JSONStorage.get_element_name(value,
                                named_args))
                else:
                    if reversed_key not in current_level:
                        current_level[reversed_key] = type(value)()
                    JSONStorage.process_scheme(
                            value,
                            current_level[reversed_key],
                            named_args
                            )

    def put_responce(self, *args) -> {"A"}: 
            named_args = {self.needed_keys[i]:arg for i, arg in
            enumerate(list(args))}
            with self.lock:
                JSONStorage.process_scheme(self.scheme, self.respdict, named_args)

    def save(self):
        with self.lock:
            print("saving")
            print(self.respdict)
            with open(self.path, "w") as f:
                json.dump(self.respdict, f, default = lambda o: o if not
                isinstance(o, set) else list(o))
        self.respdict = {}
