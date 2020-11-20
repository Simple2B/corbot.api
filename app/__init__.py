import os
import json

from flask import Flask, current_app, make_response
from flask_sqlalchemy import SQLAlchemy


from app.controllers.db_handler import DB1, DB_TEST
from app.models.vps import VPS

# instantiate extensions
db = SQLAlchemy()
db1 = DB_TEST()
if current_app and (not current_app.config["TESTING"]):
    db1 = DB1()
session = db1.session
metadata = db1.metadata

GOOD_IPS = ['127.0.0.1']  # list of authenticated IPs, localhost is added for testing


def create_app(environment="development"):
    from config import config
    from app.views import (
        main_blueprint,
    )

    # Instantiate app.
    app = Flask(__name__)
    app.db1 = db1
    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    global GOOD_IPS
    # Adding IPs valid for authentication
    res = app.db1.session.query(VPS).all()  # fetching IPs from db
    ips_from_db = [i.ip_address for i in res]
    GOOD_IPS += ips_from_db

    # address of json file relative to project root directory, it is written in .env file
    app.IP_ADDRESSES_FILE = os.environ.get('IP_ADDRESSES_FILE', "ip_addresses.json")
    with open(os.path.join('./', app.IP_ADDRESSES_FILE)) as f:
        ips_from_json = json.load(f)['ip_addresses']  # fetching IPs from json file
    GOOD_IPS += ips_from_json
    app.GOOD_IPS = GOOD_IPS

    # Set up extensions.
    db.init_app(app)

    # Register blueprints.
    app.register_blueprint(main_blueprint)

    # Error handlers.
    @app.errorhandler(Exception)
    def handle_error(exc):
        error_dict = {
            'error': exc,
            "doc": exc.__doc__
        }
        res = make_response(json.dumps(error_dict, indent=4, sort_keys=True, default=str), 400)
        res.mimetype = 'application/json'
        return res

    return app
