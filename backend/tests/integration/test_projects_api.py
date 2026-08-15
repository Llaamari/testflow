def test_create_project(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "Fictional software test project.",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Autonomous Drone Control System"
    assert data["description"] == "Fictional software test project."
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_projects(client):
    client.post(
        "/api/v1/projects",
        json={
            "name": "Autonomous Drone Control System",
            "description": "First fictional project.",
        },
    )

    client.post(
        "/api/v1/projects",
        json={
            "name": "Smart Greenhouse Monitoring Platform",
            "description": "Second fictional project.",
        },
    )

    response = client.get("/api/v1/projects")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2

def test_get_project_by_id(client):
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Warehouse Robotics Simulator",
            "description": "Fictional warehouse automation project.",
        },
    )

    created_project = create_response.get_json()
    project_id = created_project["id"]

    response = client.get(
        f"/api/v1/projects/{project_id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == project_id
    assert data["name"] == "Warehouse Robotics Simulator"

def test_get_unknown_project_returns_404(client):
    response = client.get(
        "/api/v1/projects/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "PROJECT_NOT_FOUND"

def test_get_project_with_invalid_id_returns_404(client):
    response = client.get(
        "/api/v1/projects/not-a-valid-id"
    )

    assert response.status_code == 404

def test_create_project_without_name_returns_400(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "description": "Missing project name."
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Project name is required."

def test_create_project_with_blank_name_returns_400(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "   ",
            "description": "Blank name test.",
        },
    )

    assert response.status_code == 400

def test_create_project_without_json_body_returns_400(client):
    response = client.post(
        "/api/v1/projects"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "INVALID_REQUEST"

def test_update_project(client):
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Original Project",
            "description": "Original description.",
        },
    )

    project_id = create_response.get_json()["id"]

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        json={
            "name": "Updated Project",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Updated Project"
    assert data["description"] == "Original description."

def test_update_project_with_blank_name_returns_400(client):
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Valid Project",
            "description": "",
        },
    )

    project_id = create_response.get_json()["id"]

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        json={
            "name": "   ",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_update_project_without_valid_fields_returns_400(client):
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Protected Fields Test",
            "description": "",
        },
    )

    project_id = create_response.get_json()["id"]

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        json={
            "created_at": "2020-01-01",
        },
    )

    assert response.status_code == 400

def test_update_unknown_project_returns_404(client):
    response = client.patch(
        "/api/v1/projects/507f1f77bcf86cd799439011",
        json={
            "name": "Does Not Exist",
        },
    )

    assert response.status_code == 404

def test_delete_project(client):
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Project To Delete",
            "description": "",
        },
    )

    project_id = create_response.get_json()["id"]

    delete_response = client.delete(
        f"/api/v1/projects/{project_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/projects/{project_id}"
    )

    assert get_response.status_code == 404

def test_delete_unknown_project_returns_404(client):
    response = client.delete(
        "/api/v1/projects/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"]["code"] == "PROJECT_NOT_FOUND"