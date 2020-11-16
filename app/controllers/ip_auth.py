import os
from functools import wraps
import distutils.util

from flask import request

# here one has to put all IPs of bots and any other that are going to be used to test this application
GOOD_IPS = ['127.0.0.1']


def ip_auth(a_func):

    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        IP_AUTH_ENABLED = os.environ.get("IP_AUTH_ENABLED", True)
        IP_AUTH_ENABLED = bool(distutils.util.strtobool(IP_AUTH_ENABLED))
        ip = request.remote_addr
        if IP_AUTH_ENABLED:
            if ip in GOOD_IPS:
                return a_func(*args, **kwargs)
        else:
            return a_func(*args, **kwargs)

    return wrapTheFunction
