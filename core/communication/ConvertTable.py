def convert_function(_from, _to):
    '''This decorator is simple way to declare ability of function to be
    converter from name _from to name _to in convert table'''
    def real_decorator(function):
        function.__from__ = _from
        function.__to__ = _to
        return function
    return real_decorator


class ConvertTable():
    '''The class is used to store and find the right function to convert value from
    one key to another'''
    def __init__(self):
        self.convert_functions = []

    def add_function(self, function):
        '''Here you can add function to ConvertTable.'''
        #TODO: make this method produce new functions, that will be able to
        #create converter chains
        print("adding function", function)
        self.convert_functions.append(function)

    def get_converter(self, from_keys, to_key):
        '''This function returns converter function, that can convert one key
        to another'''
        for function in self.convert_functions:
            if function.__from__ in from_keys and function.__to__ == to_key:
                return function.__from__, function
        print("Can't find converter!")
        return None, None
