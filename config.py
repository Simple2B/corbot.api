import os
from os import environ
from dotenv import load_dotenv
from app.logger import log

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Corbot API"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "DIAOIS9zEy5hLHDxi9TE5Re0THM"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = log.INFO

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOP_DATABASE_URL', f'mysql+pymysql://{environ.get("DB_USER", "user")}:{environ.get("DB_PASS", "")}@'
                                f'{environ.get("DB_IP", "localhost")}:{environ.get("DB_PORT", "3306")}/'
                                f'{environ.get("DB_NAME", "db")}')

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = log.DEBUG


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    LOG_LEVEL = log.DEBUG


class ProductionConfig(BaseConfig):
    """Production configuration."""

    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
