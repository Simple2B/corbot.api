import os
import json

from sqlalchemy import Table

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


from app.controllers.db_handler import DB1
db1 = DB1()
metadata = db1.metadata
session = db1.session

# instantiate extensions
db = SQLAlchemy()

# here one has to put all IPs of bots and any other that are going to be used to test this application
GOOD_IPS = []


def create_app(environment="development"):
    GOOD_IPS = ['127.0.0.1']

    from config import config
    from app.views import (
        main_blueprint,
    )

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Adding IPs valid for authentication
    if not app.config['TESTING']:
        vps = Table("vps", metadata, autoload=True)
        qry = vps.select()
        res = qry.execute()
        ips_from_db = [i.ip_address for i in res]
        GOOD_IPS += ips_from_db
    else:
        pass

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
