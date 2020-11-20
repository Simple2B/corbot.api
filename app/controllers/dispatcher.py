from .register import Register

import app.controllers.test  # noqa 401
import app.controllers.runner  # noqa 401


def dispatch(request_data: dict):
    method_name = request_data["request"]
    class_name = request_data["class"] if "class" in request_data else None

    method = Register.lookup(method_name, class_name)
    # res_to_json converts function responce to standart format
    return dict(request=method_name, data=method(request_data["data"]))
