def create_project(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "Fictional project.",
        },
    )

    return response.get_json()

def test_create_test_suite(client):
    project = create_project(client)

    response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
            "description": "Navigation-related test cases.",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Navigation Tests"
    assert data["project_id"] == project["id"]
    assert "id" in data

def test_create_test_suite_for_unknown_project_returns_404(client):
    response = client.post(
        "/api/v1/projects/507f1f77bcf86cd799439011/test-suites",
        json={
            "name": "Navigation Tests",
            "description": "",
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "PROJECT_NOT_FOUND"

def test_get_test_suites_for_project(client):
    project = create_project(client)

    client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
        },
    )

    client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Sensor Tests",
        },
    )

    response = client.get(
        f"/api/v1/projects/{project['id']}/test-suites"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2

def test_project_only_returns_its_own_test_suites(client):
    first_project = create_project(client)

    second_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Smart Greenhouse Monitoring Platform",
            "description": "",
        },
    )

    second_project = second_response.get_json()

    client.post(
        f"/api/v1/projects/{first_project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
        },
    )

    client.post(
        f"/api/v1/projects/{second_project['id']}/test-suites",
        json={
            "name": "Sensor Tests",
        },
    )

    response = client.get(
        f"/api/v1/projects/{first_project['id']}/test-suites"
    )

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "Navigation Tests"

def test_get_test_suite_by_id(client):
    project = create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Communication Tests",
        },
    )

    suite = create_response.get_json()

    response = client.get(
        f"/api/v1/test-suites/{suite['id']}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == suite["id"]
    assert data["name"] == "Communication Tests"

def test_update_test_suite(client):
    project = create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Old Suite Name",
            "description": "Original description.",
        },
    )

    suite = create_response.get_json()

    response = client.patch(
        f"/api/v1/test-suites/{suite['id']}",
        json={
            "name": "Performance Tests",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Performance Tests"
    assert data["description"] == "Original description."

def test_delete_test_suite(client):
    project = create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Suite To Delete",
        },
    )

    suite = create_response.get_json()

    delete_response = client.delete(
        f"/api/v1/test-suites/{suite['id']}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/test-suites/{suite['id']}"
    )

    assert get_response.status_code == 404

def test_create_test_suite_without_name_returns_400(client):
    project = create_project(client)

    response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "description": "Missing suite name.",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Test suite name is required."


def test_create_test_suite_with_blank_name_returns_400(client):
    project = create_project(client)

    response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "   ",
            "description": "Blank suite name.",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_update_test_suite_with_blank_name_returns_400(client):
    project = create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
            "description": "",
        },
    )

    suite = create_response.get_json()

    response = client.patch(
        f"/api/v1/test-suites/{suite['id']}",
        json={
            "name": "   ",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_get_unknown_test_suite_returns_404(client):
    response = client.get(
        "/api/v1/test-suites/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "TEST_SUITE_NOT_FOUND"


def test_update_unknown_test_suite_returns_404(client):
    response = client.patch(
        "/api/v1/test-suites/507f1f77bcf86cd799439011",
        json={
            "name": "Updated Suite",
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "TEST_SUITE_NOT_FOUND"


def test_delete_unknown_test_suite_returns_404(client):
    response = client.delete(
        "/api/v1/test-suites/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "TEST_SUITE_NOT_FOUND"


def test_get_test_suites_for_unknown_project_returns_404(client):
    response = client.get(
        "/api/v1/projects/507f1f77bcf86cd799439011/test-suites"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "PROJECT_NOT_FOUND"


def test_create_test_suite_with_invalid_description_returns_400(client):
    project = create_project(client)

    response = client.post(
        f"/api/v1/projects/{project['id']}/test-suites",
        json={
            "name": "Navigation Tests",
            "description": 123,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert (
        data["error"]["message"]
        == "Test suite description must be a string."
    )