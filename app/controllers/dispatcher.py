from .register import Register

import app.controllers.test  # noqa 401
import app.controllers.runner  # noqa 401
from app.logger import log


def dispatch(request_data: dict):
    log(log.DEBUG, "dispatch")
    method_name = request_data["request"]
    log(log.DEBUG, "method name: %s", method_name)
    class_name = request_data["class"] if "class" in request_data else None

    method = Register.lookup(method_name, class_name)
    # res_to_json converts function responce to standart format
    return dict(request=method_name, data=method(request_data["data"]))
