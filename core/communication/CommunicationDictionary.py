class CommunicationDictionary(dict):
    '''This class is used to provide communication between classes using
    key-value interface'''
    def __init__(self, convert_table):
        '''Convert table stores functions used to get value of unable key if
        it's possible'''
        super(CommunicationDictionary, self).__init__()
        self.convert_table = convert_table

    def __getitem__(self, key):
        item = None
        try:
            item = dict.__getitem__(self,key)
        except KeyError:
            key_to_convert, convert_function = self.convert_table.get_converter(
                self.keys(),
                key
            )
            if key_to_convert is not None:
                item = convert_function(dict.__getitem__(self,key_to_convert))

        return item
