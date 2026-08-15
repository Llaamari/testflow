import pytest

from app import create_app
from app.config import TestingConfig
from app.database import get_database


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    yield app

    database = get_database()
    database["test_results"].delete_many({})
    database["test_runs"].delete_many({})
    database["test_suites"].delete_many({})
    database["projects"].delete_many({})


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def project(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "Fictional project.",
        },
    )

    assert response.status_code == 201

    return response.get_json()


@pytest.fixture()
def test_suite(client, project):
    response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
            "description": "Fictional test suite.",
        },
    )

    assert response.status_code == 201

    return response.get_json()


@pytest.fixture()
def test_run(client, project, test_suite):
    response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": test_suite["id"],
            "software_version": "2.4.0",
        },
    )

    assert response.status_code == 201

    return response.get_json()