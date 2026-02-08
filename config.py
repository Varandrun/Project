import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'journal_platform.sqlite')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
