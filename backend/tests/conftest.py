import pytest

from app import create_app
from app.config import TestingConfig
from app.database import get_database


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    yield app

    database = get_database()
    database["test_runs"].delete_many({})
    database["test_suites"].delete_many({})
    database["projects"].delete_many({})


@pytest.fixture()
def client(app):
    return app.test_client()