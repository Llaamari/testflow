from io import BytesIO

import pandas as pd

def create_project(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "Fictional project.",
        },
    )

    assert response.status_code == 201
    return response.get_json()


def create_suite(client, project_id):
    response = client.post(
        f"/api/v1/projects/{project_id}/test-suites",
        json={
            "name": "Navigation Tests",
            "description": "Fictional test suite.",
        },
    )

    assert response.status_code == 201
    return response.get_json()


def create_run(client, project_id, suite_id):
    response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project_id,
            "test_suite_id": suite_id,
            "software_version": "2.4.0",
        },
    )

    assert response.status_code == 201
    return response.get_json()


def test_import_parquet_results(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    dataframe = pd.DataFrame(
        {
            "test_name": [
                "waypoint_navigation",
                "gps_signal_loss_recovery",
            ],
            "status": [
                "PASSED",
                "FAILED",
            ],
            "duration_ms": [
                100,
                250,
            ],
            "timestamp": [
                "2026-08-15T18:30:00Z",
                "2026-08-15T18:31:00Z",
            ],
        }
    )

    buffer = BytesIO()

    dataframe.to_parquet(
        buffer,
        engine="pyarrow",
        index=False,
    )

    buffer.seek(0)

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/parquet",
        data={
            "file": (
                buffer,
                "results.parquet",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["imported_count"] == 2
    assert data["run_status"] == "FAILED"

    results_response = client.get(
        f"/api/v1/test-runs/{run['id']}/results"
    )

    results = results_response.get_json()

    assert len(results) == 2


def test_corrupted_parquet_returns_422(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/parquet",
        data={
            "file": (
                BytesIO(b"invalid parquet content"),
                "results.parquet",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 422

    data = response.get_json()

    assert data["error"]["code"] == "INVALID_IMPORT_DATA"


def test_parquet_import_without_file_returns_400(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/parquet",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "INVALID_FILE_UPLOAD"