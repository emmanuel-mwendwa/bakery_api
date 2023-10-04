from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app

    db.init_app(app)

    from .production import production as production_blueprint
    app.register_blueprint(production_blueprint, url_prefix='/production')

    return app