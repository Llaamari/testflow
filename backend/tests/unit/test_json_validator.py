from app.models.status import TestStatus
from app.validators.json_validator import validate_json_results


def test_valid_json_results_are_normalized():
    payload = {
        "results": [
            {
                "test_name": " waypoint_navigation ",
                "status": "PASSED",
                "duration_ms": 123,
                "timestamp": "2026-08-15T18:30:00Z",
            }
        ]
    }

    results, errors = validate_json_results(payload)

    assert errors == []
    assert results is not None
    assert len(results) == 1

    result = results[0]

    assert result["test_name"] == "waypoint_navigation"
    assert result["status"] == TestStatus.PASSED
    assert result["duration_ms"] == 123.0


def test_empty_results_array_returns_error():
    results, errors = validate_json_results(
        {"results": []}
    )

    assert results is None
    assert len(errors) == 1
    assert errors[0]["field"] == "results"


def test_multiple_validation_errors_are_returned():
    payload = {
        "results": [
            {
                "test_name": "",
                "status": "SUCCESS",
                "duration_ms": -1,
            }
        ]
    }

    results, errors = validate_json_results(payload)

    assert results is None

    fields = {
        error["field"]
        for error in errors
    }

    assert "test_name" in fields
    assert "status" in fields
    assert "duration_ms" in fields