def get_argument_annotations(func):
    return list(value for key, value in func.__annotations__.items() if key !=
    'return')

def get_return_annotations(func):
    return func.__annotations__['return']

def complitable_functions(output_function, input_function, convert_table):
    input_keys = set(get_argument_annotations(input_function))
    return_keys = set(get_return_annotations(output_function))
    all_possible_return_keys = return_keys.union(
        convert_table.all_possible_conversions(return_keys)
    )
    print("return:%s\npossible_output:%s" % (return_keys,
    all_possible_return_keys))
    return input_keys.issubset(all_possible_return_keys)

def get_converted_arguments(function, simple_arg_dict, convert_table):
    #This function returns list of arguments needed by function made from
    #simple_arg_dict by convert_table
    if simple_arg_dict == None:
        return [None for key in function.__annotations__.keys() if key != 'return']
    result = []
    if not hasattr(function, "__annotations__"):
        return result
    for key, value in function.__annotations__.items():
        if key != 'return':
            converted_arg = None
            try:
                converted_arg = simple_arg_dict[value]
            except KeyError:
                key_to_convert, convert_function = convert_table.get_converter(
                    simple_arg_dict.keys(),
                    value
                    )
                key_to_convert = list(key_to_convert)[0]
                converted_arg = convert_function(
                    simple_arg_dict[key_to_convert]
                    )[value]
            result.append(converted_arg)
    return result
