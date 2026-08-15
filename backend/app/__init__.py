from flask import Flask

from app.config import DevelopmentConfig
from app.routes.health import health_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(
        health_bp,
        url_prefix="/api/v1",
    )

    return app