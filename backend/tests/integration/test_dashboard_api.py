def test_dashboard_stats_are_zero_when_database_is_empty(client):
    response = client.get(
        "/api/v1/dashboard/stats"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["projects"] == 0
    assert data["test_runs"] == 0
    assert data["test_results"] == 0
    assert data["pass_rate"] == 0.0
    assert data["failed"] == 0
    assert data["errors"] == 0
    assert data["pending"] == 0

    assert data["status_distribution"] == {
        "PASSED": 0,
        "FAILED": 0,
        "ERROR": 0,
        "PENDING": 0,
    }

    assert data["recent_runs"] == []

def test_dashboard_stats_count_existing_data(
    client,
    test_run,
):
    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "passing_test",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "failing_test",
            "status": "FAILED",
            "duration_ms": 150,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "error_test",
            "status": "ERROR",
            "duration_ms": 50,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "pending_test",
            "status": "PENDING",
            "duration_ms": 0,
        },
    )

    response = client.get(
        "/api/v1/dashboard/stats"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["projects"] == 1
    assert data["test_runs"] == 1
    assert data["test_results"] == 4

    assert data["status_distribution"] == {
        "PASSED": 1,
        "FAILED": 1,
        "ERROR": 1,
        "PENDING": 1,
    }

    assert data["failed"] == 1
    assert data["errors"] == 1
    assert data["pending"] == 1
    assert data["pass_rate"] == 33.3

def test_pending_results_do_not_reduce_pass_rate(
    client,
    test_run,
):
    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "passed_test",
            "status": "PASSED",
            "duration_ms": 100,
        },
    )

    client.post(
        f"/api/v1/test-runs/{test_run['id']}/results",
        json={
            "test_name": "pending_test",
            "status": "PENDING",
            "duration_ms": 0,
        },
    )

    response = client.get(
        "/api/v1/dashboard/stats"
    )

    data = response.get_json()

    assert data["pass_rate"] == 100.0

def test_dashboard_returns_recent_runs(
    client,
    test_run,
):
    response = client.get(
        "/api/v1/dashboard/stats"
    )

    data = response.get_json()

    assert len(data["recent_runs"]) == 1

    recent_run = data["recent_runs"][0]

    assert recent_run["id"] == test_run["id"]
    assert recent_run["run_id"] == test_run["run_id"]

def test_dashboard_returns_at_most_five_recent_runs(
    client,
    project,
    test_suite,
):
    for index in range(7):
        response = client.post(
            "/api/v1/test-runs",
            json={
                "project_id": project["id"],
                "test_suite_id": test_suite["id"],
                "software_version": f"1.0.{index}",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/dashboard/stats"
    )

    data = response.get_json()

    assert len(data["recent_runs"]) == 5