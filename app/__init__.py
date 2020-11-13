import os
import json

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


from app.controllers.db_handler import DB1
db1 = DB1()
metadata = db1.metadata
session = db1.session


# instantiate extensions
db = SQLAlchemy()


def create_app(environment="development"):

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
