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

def test_import_json_results(client, test_run):
    response = client.post(
        f"/api/v1/test-runs/{test_run['id']}/results/import/json",
        json={
            "results": [
                {
                    "test_name": "test_one",
                    "status": "PASSED",
                    "duration_ms": 100,
                },
                {
                    "test_name": "test_two",
                    "status": "FAILED",
                    "duration_ms": 200,
                },
            ]
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["imported_count"] == 2
    assert data["run_status"] == "FAILED"

    results_response = client.get(
        f"/api/v1/test-runs/{test_run['id']}/results"
    )

    results = results_response.get_json()

    assert len(results) == 2

def test_json_import_aggregates_with_existing_results(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    client.post(
        f"/api/v1/test-runs/{run['id']}/results",
        json={
            "test_name": "existing_error",
            "status": "ERROR",
            "duration_ms": 50,
        },
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/json",
        json={
            "results": [
                {
                    "test_name": "new_pass",
                    "status": "PASSED",
                    "duration_ms": 100,
                }
            ]
        },
    )

    assert response.status_code == 201
    assert response.get_json()["run_status"] == "ERROR"

def test_json_import_with_invalid_status_returns_422(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/json",
        json={
            "results": [
                {
                    "test_name": "invalid_test",
                    "status": "SUCCESS",
                    "duration_ms": 100,
                }
            ]
        },
    )

    assert response.status_code == 422

    data = response.get_json()

    assert data["error"]["code"] == "INVALID_IMPORT_DATA"
    assert len(data["error"]["details"]) > 0

def test_invalid_json_import_does_not_store_partial_results(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results/import/json",
        json={
            "results": [
                {
                    "test_name": "valid_test",
                    "status": "PASSED",
                    "duration_ms": 100,
                },
                {
                    "test_name": "invalid_test",
                    "status": "SUCCESS",
                    "duration_ms": 200,
                },
            ]
        },
    )

    assert response.status_code == 422

    results_response = client.get(
        f"/api/v1/test-runs/{run['id']}/results"
    )

    assert results_response.get_json() == []