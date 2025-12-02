import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    # For local development prefer a lightweight sqlite DB unless the
    # `DATABASE_URI` environment variable is provided. This avoids failing
    # to start the app when MySQL isn't configured on the machine.
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI")
        or "sqlite:///dev.db"
    )


class ProdConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


config = {"development": DevConfig, "production": ProdConfig, "default": DevConfig}
