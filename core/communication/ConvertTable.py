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
                print("found converter for %s!!!" % to_key)
                return input_args, function
        raise Exception("There is no converter for %s to %s" % (from_keys,
        to_key))
        return None, None

    def get_metaconverter(self, from_keys, to_keys):
        '''This function constructs and returns new function used to provide fast
        conversion from from_keys to to_keys'''
        print("from_keys",from_keys)
        print("to_keys",to_keys)
        converters_args = [] 
        converters = []
        for key in to_keys:
            keys_to_convert, converter = None, None
            if key in from_keys:
                print("%s is in from_keys" % key)
                keys_to_convert = [key]
                converter = lambda x : {key: x}
            else:
                print("getting converter for %s." % key)
                keys_to_convert, converter = self.get_converter(from_keys, key)
                print("needed keys: %s" % " ".join(keys_to_convert))
            converters_args.append(keys_to_convert)
            converters.append(converter)
        def metaconverter(args_dict):
            if args_dict == None:
                return [None] * len(converters)
            res = []
            print(converters)
            print(converters_args)
            for i,conv in enumerate(converters):
                print(converters_args[i])
                print(args_dict)
                args = [args_dict[arg] for arg in converters_args[i]]
                res.append(*[value for key, value in conv(*args).items()])
            return res
        return metaconverter
