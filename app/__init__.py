import os
import json

from sqlalchemy import Table

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


from app.controllers.db_handler import DB1

# instantiate extensions
db = SQLAlchemy()

metadata = None

GOOD_IPS = ['127.0.0.1']  # list of authenticated IPs, localhost is added for testing


def create_app(environment="development"):
    from config import config
    from app.views import (
        main_blueprint,
    )

    # Instantiate app.
    app = Flask(__name__)
    db1 = DB1()
    app.db1 = db1
    global metadata
    metadata = app.db1.metadata
    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    global GOOD_IPS
    # Adding IPs valid for authentication
    vps = Table("vps", app.db1.metadata, autoload=True)  # fetching IPs from db
    qry = vps.select()
    res = qry.execute()
    ips_from_db = [i.ip_address for i in res]
    GOOD_IPS += ips_from_db

    # address of json file relative to project root directory, it is written in .env file
    app.IP_ADDRESSES_FILE = os.environ.get('IP_ADDRESSES_FILE')
    with open(os.path.join('./', app.IP_ADDRESSES_FILE)) as f:
        ips_from_json = json.load(f)['ip_addresses']  # fetching IPs from json file
    GOOD_IPS += ips_from_json
    app.GOOD_IPS = GOOD_IPS

    # Set up extensions.
    db.init_app(app)

    # Register blueprints.
    app.register_blueprint(main_blueprint)

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        error_dict = {
            'error': exc,
            "code": exc.code
        }
        # return render_template("error.html", error=exc), exc.code
        return json.dumps(error_dict, indent=4, sort_keys=True, default=str)

    return app
