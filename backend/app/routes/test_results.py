from datetime import datetime

from flask import Blueprint, jsonify, request

from app.database import get_database
from app.models.status import TestStatus
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository
from app.services.test_result_service import TestResultService
from app.utils.serialization import serialize_document


test_results_bp = Blueprint("test_results", __name__)


def get_test_result_service() -> TestResultService:
    database = get_database()

    return TestResultService(
        TestResultRepository(database),
        TestRunRepository(database),
    )

@test_results_bp.get("/test-runs/<test_run_id>/results")
def get_test_results(test_run_id: str):
    service = get_test_result_service()

    results = service.get_results(test_run_id)

    if results is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return jsonify(
        [serialize_document(result) for result in results]
    )

@test_results_bp.post("/test-runs/<test_run_id>/results")
def create_test_result(test_run_id: str):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body must contain valid JSON.",
                }
            }
        ), 400

    test_name = data.get("test_name")
    status_value = data.get("status")
    duration_ms = data.get("duration_ms")
    timestamp_value = data.get("timestamp")
    error_message = data.get("error_message")
    measurements = data.get("measurements")

    if not isinstance(test_name, str) or not test_name.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Test name is required.",
                    }
            }
        ), 400

    try:
        status = TestStatus(status_value)
    except (ValueError, TypeError):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": (
                        "Status must be one of: "
                        "PASSED, FAILED, ERROR, PENDING."
                    ),
                }
            }
        ), 400

    if (
        not isinstance(duration_ms, (int, float))
        or isinstance(duration_ms, bool)
        or duration_ms < 0
    ):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": (
                        "Duration must be a non-negative number."
                    ),
                }
            }
        ), 400

    timestamp = None

    if timestamp_value is not None:
        if not isinstance(timestamp_value, str):
            return jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Timestamp must be an ISO 8601 string.",
                    }
                }
            ), 400

        try:
            timestamp = datetime.fromisoformat(
                timestamp_value.replace("Z", "+00:00")
            )
        except ValueError:
            return jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Timestamp must be a valid ISO 8601 value.",
                    }
                }
            ), 400

    if error_message is not None and not isinstance(
        error_message,
        str,
    ):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Error message must be a string.",
                }
            }
        ), 400

    if measurements is not None and not isinstance(
        measurements,
        dict,
    ):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Measurements must be a JSON object.",
                }
            }
        ), 400

    service = get_test_result_service()

    result = service.create_result(
        test_run_id=test_run_id,
        test_name=test_name.strip(),
        status=status,
        duration_ms=float(duration_ms),
        timestamp=timestamp,
        error_message=error_message,
        measurements=measurements,
    )

    if result is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return jsonify(
        serialize_document(result)
    ), 201