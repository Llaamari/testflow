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