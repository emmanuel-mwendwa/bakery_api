import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_ADMIN = os.environ.get("APP_ADMIN")
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}