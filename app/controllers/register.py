from collections.abc import Callable


__MAP = {}


class Register(object):
    def __init__(self, class_name: str):
        self.class_name = class_name

    def add_method_on_map(self, method_name: str, method_func: Callable[[dict], dict]) -> None:
        if self.class_name not in __MAP:
            __MAP[self.class_name] = {}
        __MAP[self.class_name][method_name] = method_func

    def register(self):
        """register function in the map
        """
        def decorator(f):
            self.add_method_on_map(f.__name__, f)
            return f

        return decorator

    @staticmethod
    def lookup(method_name, class_name=None):
        if class_name:
            if class_name not in __MAP:
                raise NameError(f'The class [{class_name}] is not registered')
            if method_name not in __MAP[class_name]:
                raise NameError(f'The method [{method_name}] is not registered for the class [{class_name}]')
            return __MAP[class_name][method_name]
        for class_name in __MAP:
            if method_name in __MAP[class_name]:
                return __MAP[class_name][method_name]
        raise NameError(f'The method [{method_name}] is not registered')
