class ConvertTable():
    '''The class is used to store and find the right function to convert value from
    one key to another'''
    def __init__(self):
        self.convert_functions = []

    def add_function(self, function):
        '''Here you can add function to ConvertTable.'''
        #TODO: make this method produce new functions, that will be able to
        #create converter chains
        self.convert_functions.append(function)

    def all_possible_conversions(self, from_keys):
        result = set()
        from_keys = set(from_keys)
        for function in self.convert_functions:
            input_args = set(value for key, value in
            function.__annotations__.items() if
            key!='return')
            if input_args.issubset(from_keys):
                result = result.union(set(function.__annotations__['return']))
        return result

    def get_converter(self, from_keys, to_key):
        '''This function returns converter function, that can convert one key
        to another'''
        to_key = {to_key}
        for function in self.convert_functions:
            input_args = set(value for key, value in
            function.__annotations__.items() if
            key!='return')
            if input_args.issubset(from_keys) and to_key.issubset(function.__annotations__['return']):
                return input_args, function
        raise Exception("There is no converter for %s to %s" % (from_keys,
        to_key))
        return None, None
