import os
from functools import wraps

from flask import request

from app import GOOD_IPS

# for disable IP authorization set IP_AUTH_ENABLED in .env to value N
IP_AUTH_ENABLED = not os.environ.get("IP_AUTH_ENABLED", "Y") in ("n", "N", "False", "false", "0")


def ip_auth(a_func):

    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        ip = request.remote_addr
        if IP_AUTH_ENABLED:
            if ip in GOOD_IPS:
                return a_func(*args, **kwargs)
        else:
            return a_func(*args, **kwargs)

    return wrapTheFunction
