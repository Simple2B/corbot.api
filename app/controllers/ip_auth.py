import os
import json
from functools import wraps
from app.models.vps import VPS


from flask import request

GOOD_IPS = None
IP_ADDRESSES_FILE = os.environ.get('IP_ADDRESSES_FILE', "ip_addresses.json")

# for disable IP authorization set IP_AUTH_ENABLED in .env to value N
IP_AUTH_ENABLED = not os.environ.get("IP_AUTH_ENABLED", "Y") in ("n", "N", "False", "false", "0")


def ip_auth(a_func):

    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        global GOOD_IPS
        if not GOOD_IPS:
            GOOD_IPS = ['127.0.0.1']
            # Adding IPs valid for authentication
            res = VPS.query.all()  # fetching IPs from db
            ips_from_db = [i.ip_address for i in res]
            GOOD_IPS += ips_from_db

            # address of json file relative to project root directory, it is written in .env file

            with open(os.path.join('./', IP_ADDRESSES_FILE)) as f:
                ips_from_json = json.load(f)['ip_addresses']  # fetching IPs from json file
            GOOD_IPS += ips_from_json

        ip = request.remote_addr
        if IP_AUTH_ENABLED:
            if ip in GOOD_IPS:
                return a_func(*args, **kwargs)
        else:
            return a_func(*args, **kwargs)

    return wrapTheFunction
