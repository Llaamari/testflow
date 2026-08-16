from flask import Flask

from app.config import DevelopmentConfig
from app.database import init_database
from app.routes.health import health_bp
from app.routes.projects import projects_bp
from app.routes.test_suites import test_suites_bp
from app.routes.test_runs import test_runs_bp
from app.routes.test_results import test_results_bp
from app.routes.imports import imports_bp
from app.database import create_indexes, init_database
from app.routes.dashboard import dashboard_bp
from flask_cors import CORS


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:4200"
            }
        },
    )

    init_database(app.config["MONGO_URI"])
    create_indexes()

    app.register_blueprint(
        health_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        projects_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        test_suites_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        test_runs_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        test_results_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        imports_bp,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        dashboard_bp,
        url_prefix="/api/v1",
    )

    return app