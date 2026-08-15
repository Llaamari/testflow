from flask import Flask

from app.config import DevelopmentConfig
from app.database import init_database
from app.routes.health import health_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_database(app.config["MONGO_URI"])

    app.register_blueprint(
        health_bp,
        url_prefix="/api/v1",
    )

    return app