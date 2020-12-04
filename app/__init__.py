import os
import json

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from app.logger import log


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
    log.set_level(app.config["LOG_LEVEL"])

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
