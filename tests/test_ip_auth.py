import os
import pytest
import json

from sqlalchemy import Table

from flask import current_app

from app import create_app


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        yield client
        app_ctx.pop()


def test_ip_auth(client):
    IP_ADDRESSES_FILE = current_app.IP_ADDRESSES_FILE  # address of json file relative to project root directory
    with open(os.path.join('./', IP_ADDRESSES_FILE)) as f:
        ips_from_json = json.load(f)['ip_addresses']  # fetching IPs from json file
    for i in ips_from_json:
        assert i in current_app.GOOD_IPS  # checking that each IP from json file got to list of authenticated IPs
    vps = Table("vps", current_app.db1.metadata, autoload=True)  # fetching IPs from db
    qry = vps.select()
    res = qry.execute()
    ips_from_db = [i.ip_address for i in res]
    for i in ips_from_db:
        assert i in current_app.GOOD_IPS  # checking that each IP from db got to list of authenticated IPs
