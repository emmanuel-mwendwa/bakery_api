import os

class Config():
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


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