from functools import wraps

from flask import request

GOOD_IPS = ['46.101.202.101']


def ip_login(a_func):

    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        ip = request.remote_addr
        if ip in GOOD_IPS:
            return a_func(*args, **kwargs)

    return wrapTheFunction
