class AbstractModuleClassType(type):

    def __new__(self, name, bases, attrs):
        print("creating class", name)
        base_class = None
        if len(bases) != 0:
            base_class = bases[0]
        input_function_names = None
        output_function_names = None
        if base_class:
            input_function_names = getattr(base_class, "INPUT_FUNCTIONS")
            output_function_names = getattr(base_class, "OUTPUT_FUNCTIONS")
        else:
            input_function_names = attrs["INPUT_FUNCTIONS"]
            output_function_names = attrs["OUTPUT_FUNCTIONS"]

        if not name.startswith("Abstract"):
            for attrname, attrvalue in attrs.items():
                if type(attrvalue).__name__ == 'function':
                    if attrvalue.__name__ in input_function_names:
                        if len(list(filter(lambda x: x!= "return",
                            attrvalue.__annotations__.keys()))) == 0:
                            raise Exception(
                                    "%s.%s:no input annotations." %
                                    (name, attrname)
                                    )
                    if attrvalue.__name__ in output_function_names:
                            try:
                                attrvalue.__annotations__["return"]
                            except KeyError:
                                raise Exception(
                                    "%s.%s: return type is not defined!" % 
                                    (name, attrname)
                                )
        return super().__new__(self, name, bases, attrs)

class AbstractModuleClass(metaclass = AbstractModuleClassType):
    REQUIED_INPUT_KEYS = None
    OUTPUT_KEYS = []
    INPUT_FUNCTIONS = {}
    OUTPUT_FUNCTIONS = {}
