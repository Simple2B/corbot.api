import os
from os import environ

base_dir = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Flask App"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOP_DATABASE_URL', f'mysql+pymysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@'
                                f'{environ.get("DB_IP")}:{str(environ.get("DB_PORT"))}/'
                                f'{environ.get("DB_NAME")}')

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
