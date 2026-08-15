def create_project(client, name="Autonomous Drone Control System"):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": name,
            "description": "Fictional project.",
        },
    )

    return response.get_json()


def create_suite(client, project_id, name="Navigation Tests"):
    response = client.post(
        f"/api/v1/projects/{project_id}/test-suites",
        json={
            "name": name,
            "description": "Fictional suite.",
        },
    )

    return response.get_json()


def test_create_test_run(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])

    response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
            "software_version": "2.4.0",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["project_id"] == project["id"]
    assert data["test_suite_id"] == suite["id"]
    assert data["software_version"] == "2.4.0"
    assert data["status"] == "PENDING"
    assert data["run_id"].startswith("RUN-")
    assert data["completed_at"] is None


def test_create_test_run_with_suite_from_another_project_returns_404(client):
    first_project = create_project(
        client,
        "Autonomous Drone Control System",
    )

    second_project = create_project(
        client,
        "Smart Greenhouse Monitoring Platform",
    )

    suite = create_suite(
        client,
        first_project["id"],
    )

    response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": second_project["id"],
            "test_suite_id": suite["id"],
            "software_version": "1.0.0",
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "INVALID_TEST_RUN_RELATION"


def test_get_test_runs(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])

    client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
            "software_version": "2.4.0",
        },
    )

    client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
            "software_version": "2.5.0",
        },
    )

    response = client.get("/api/v1/test-runs")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2


def test_get_test_run_by_id(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])

    create_response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
            "software_version": "3.1.0",
        },
    )

    created = create_response.get_json()

    response = client.get(
        f"/api/v1/test-runs/{created['id']}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == created["id"]
    assert data["run_id"] == created["run_id"]


def test_delete_test_run(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])

    create_response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
            "software_version": "1.2.0",
        },
    )

    created = create_response.get_json()

    delete_response = client.delete(
        f"/api/v1/test-runs/{created['id']}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/test-runs/{created['id']}"
    )

    assert get_response.status_code == 404


def test_create_test_run_without_software_version_returns_400(client):
    project = create_project(client)
    suite = create_suite(client, project["id"])

    response = client.post(
        "/api/v1/test-runs",
        json={
            "project_id": project["id"],
            "test_suite_id": suite["id"],
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_get_unknown_test_run_returns_404(client):
    response = client.get(
        "/api/v1/test-runs/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "TEST_RUN_NOT_FOUND"