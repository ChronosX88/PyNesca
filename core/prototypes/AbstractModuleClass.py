def internal(func):
    func.is_internal = True
    return func

class AbstractModuleClassType(type):

    def __new__(self, name, bases, attrs):
        print("creating class", name)
        if not name.startswith("Abstract"):
            for attrname, attrvalue in attrs.items():
                if type(attrvalue).__name__ == 'function':
                    if attrvalue.__name__ not in ["__init__", "save"] and not (hasattr(attrvalue, "is_internal") and attrvalue.is_internal
                    ):
                        if not name.endswith("Storage"):
                            try:
                                attrvalue.__annotations__["return"]
                            except KeyError:
                                raise Exception(
                                    "%s.%s: return type is not defined!" % 
                                    (name, attrname)
                                )
                        if not name.endswith("Parser"):
                            if not attrvalue.__annotations__:
                                raise Exception(
                                    "%s.%s: arguments missing annotations!" %
                                    (name, attrname)
                                    )
        return super().__new__(self, name, bases, attrs)

class AbstractModuleClass(metaclass = AbstractModuleClassType):
    REQUIED_INPUT_KEYS = None
    OUTPUT_KEYS = []
