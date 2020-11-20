from typing import Callable


_MAP = {}


class Register(object):
    def __init__(self, class_name: str):
        self.class_name = class_name

    def add_method_on_map(self, method_name: str, method_func: Callable[[dict], dict]) -> None:
        if self.class_name not in _MAP:
            _MAP[self.class_name] = {}
        _MAP[self.class_name][method_name] = method_func

    def register(self, **options):
        """register function in the map
        """

        def decorator(func):
            if "name" in options:
                self.add_method_on_map(options["name"], func)
            else:
                self.add_method_on_map(func.__name__, func)
            return func

        return decorator

    @staticmethod
    def lookup(method_name, class_name=None):
        if class_name:
            if class_name not in _MAP:
                raise NameError(f'The class [{class_name}] is not registered')
            if method_name not in _MAP[class_name]:
                raise NameError(f'The method [{method_name}] is not registered for the class [{class_name}]')
            return _MAP[class_name][method_name]
        for class_name in _MAP:
            if method_name in _MAP[class_name]:
                return _MAP[class_name][method_name]
        raise NameError(f'The method [{method_name}] is not registered')
