from flask import Blueprint, jsonify, request

from app.database import get_database
from app.repositories.project_repository import ProjectRepository
from app.repositories.test_run_repository import TestRunRepository
from app.repositories.test_suite_repository import TestSuiteRepository
from app.services.test_run_service import TestRunService
from app.utils.serialization import serialize_document


test_runs_bp = Blueprint("test_runs", __name__)


def get_test_run_service() -> TestRunService:
    database = get_database()

    return TestRunService(
        TestRunRepository(database),
        ProjectRepository(database),
        TestSuiteRepository(database),
    )


@test_runs_bp.get("/test-runs")
def get_test_runs():
    service = get_test_run_service()

    runs = service.get_runs()

    return jsonify(
        [serialize_document(run) for run in runs]
    )


@test_runs_bp.get("/test-runs/<test_run_id>")
def get_test_run(test_run_id: str):
    service = get_test_run_service()

    run = service.get_run(test_run_id)

    if run is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return jsonify(
        serialize_document(run)
    )


@test_runs_bp.post("/test-runs")
def create_test_run():
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

    project_id = data.get("project_id")
    test_suite_id = data.get("test_suite_id")
    software_version = data.get("software_version")

    if not isinstance(project_id, str) or not project_id.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Project ID is required.",
                }
            }
        ), 400

    if not isinstance(test_suite_id, str) or not test_suite_id.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Test suite ID is required.",
                }
            }
        ), 400

    if (
        not isinstance(software_version, str)
        or not software_version.strip()
    ):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Software version is required.",
                }
            }
        ), 400

    service = get_test_run_service()

    run = service.create_run(
        project_id=project_id.strip(),
        test_suite_id=test_suite_id.strip(),
        software_version=software_version.strip(),
    )

    if run is None:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_TEST_RUN_RELATION",
                    "message": (
                        "Project or test suite was not found, "
                        "or the test suite does not belong to the project."
                    ),
                }
            }
        ), 404

    return jsonify(
        serialize_document(run)
    ), 201


@test_runs_bp.delete("/test-runs/<test_run_id>")
def delete_test_run(test_run_id: str):
    service = get_test_run_service()

    deleted = service.delete_run(test_run_id)

    if not deleted:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return "", 204