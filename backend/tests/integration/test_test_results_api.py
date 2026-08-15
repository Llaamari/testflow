def create_project(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "Fictional project.",
        },
    )

    return response.get_json()


def create_suite(client, project_id):
    response = client.post(
        f"/api/v1/projects/{project_id}/test-suites",
        json={
            "name": "Navigation Tests",
        },
    )

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

    return response.get_json()


def test_create_test_result(client, test_run):
    response = client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "waypoint_navigation",
            "status": "PASSED",
            "duration_ms": 183.5,
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["test_name"] == "waypoint_navigation"
    assert data["status"] == "PASSED"
    assert data["duration_ms"] == 183.5
    assert data["test_run_id"] == test_run["id"]


def test_run_status_becomes_passed_after_passed_result(
    client,
    test_run,
):
    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "waypoint_navigation",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    response = client.get(
        f"/api/v1/test-runs/{test_run['id']}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "PASSED"


def test_failed_result_changes_run_status_to_failed(
    client,
    test_run,
):
    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "test_one",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "test_two",
            "status": "FAILED",
            "duration_ms": 200,
        },
    )

    response = client.get(
        f"/api/v1/test-runs/{test_run['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "FAILED"


def test_error_result_has_highest_priority(
    client,
    test_run,
):
    for status in [
        "PASSED",
        "FAILED",
        "ERROR",
        "PENDING",
    ]:
        response = client.post(
            f"/api/v1/test-runs/{test_run['id']}/results",
            json={
                "test_name": f"test_{status.lower()}",
                "status": status,
                "duration_ms": 100,
            },
        )

        assert response.status_code == 201

    response = client.get(
        f"/api/v1/test-runs/{test_run['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "ERROR"


def test_pending_result_keeps_priority_over_passed(
    client,
    test_run,
):
    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "finished_test",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "unfinished_test",
            "status": "PENDING",
            "duration_ms": 0,
        },
    )

    response = client.get(
        f"/api/v1/test-runs/{test_run['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "PENDING"


def test_get_results_for_test_run(client):
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
            "test_name": "test_one",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    client.post(
        f"/api/v1/test-runs/{run['id']}/results",
        json={
            "test_name": "test_two",
            "status": "FAILED",
            "duration_ms": 200,
        },
    )

    response = client.get(
        f"/api/v1/test-runs/{run['id']}/results"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2


def test_create_result_with_invalid_status_returns_400(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])
    run = create_run(
        client,
        project["id"],
        suite["id"],
    )

    response = client.post(
        f"/api/v1/test-runs/{run['id']}/results",
        json={
            "test_name": "invalid_status_test",
            "status": "SUCCESS",
            "duration_ms": 100,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"