from flask import Blueprint, jsonify, request

from app.database import get_database
from app.repositories.project_repository import ProjectRepository
from app.repositories.test_suite_repository import TestSuiteRepository
from app.services.test_suite_service import TestSuiteService
from app.utils.serialization import serialize_document


test_suites_bp = Blueprint("test_suites", __name__)


def get_test_suite_service() -> TestSuiteService:
    database = get_database()

    suite_repository = TestSuiteRepository(database)
    project_repository = ProjectRepository(database)

    return TestSuiteService(
        suite_repository,
        project_repository,
    )


@test_suites_bp.get("/projects/<project_id>/test-suites")
def get_test_suites(project_id: str):
    service = get_test_suite_service()

    suites = service.get_suites_for_project(project_id)

    if suites is None:
        return jsonify(
            {
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": "Project was not found.",
                }
            }
        ), 404

    return jsonify(
        [serialize_document(suite) for suite in suites]
    )


@test_suites_bp.post("/projects/<project_id>/test-suites")
def create_test_suite(project_id: str):
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

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Test suite name is required.",
                }
            }
        ), 400

    description = data.get("description", "")

    if not isinstance(description, str):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Test suite description must be a string.",
                }
            }
        ), 400

    service = get_test_suite_service()

    suite = service.create_suite(
        project_id=project_id,
        name=name.strip(),
        description=description.strip(),
    )

    if suite is None:
        return jsonify(
            {
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": "Project was not found.",
                }
            }
        ), 404

    return jsonify(
        serialize_document(suite)
    ), 201


@test_suites_bp.get("/test-suites/<suite_id>")
def get_test_suite(suite_id: str):
    service = get_test_suite_service()

    suite = service.get_suite(suite_id)

    if suite is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_SUITE_NOT_FOUND",
                    "message": "Test suite was not found.",
                }
            }
        ), 404

    return jsonify(
        serialize_document(suite)
    )


@test_suites_bp.patch("/test-suites/<suite_id>")
def update_test_suite(suite_id: str):
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

    updates = {}

    if "name" in data:
        name = data["name"]

        if not isinstance(name, str) or not name.strip():
            return jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Test suite name must be a non-empty string.",
                    }
                }
            ), 400

        updates["name"] = name.strip()

    if "description" in data:
        description = data["description"]

        if not isinstance(description, str):
            return jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Test suite description must be a string.",
                    }
                }
            ), 400

        updates["description"] = description.strip()

    if not updates:
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "No valid test suite fields were provided.",
                }
            }
        ), 400

    service = get_test_suite_service()

    suite = service.update_suite(
        suite_id,
        updates,
    )

    if suite is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_SUITE_NOT_FOUND",
                    "message": "Test suite was not found.",
                }
            }
        ), 404

    return jsonify(
        serialize_document(suite)
    )


@test_suites_bp.delete("/test-suites/<suite_id>")
def delete_test_suite(suite_id: str):
    service = get_test_suite_service()

    deleted = service.delete_suite(suite_id)

    if not deleted:
        return jsonify(
            {
                "error": {
                    "code": "TEST_SUITE_NOT_FOUND",
                    "message": "Test suite was not found.",
                }
            }
        ), 404

    return "", 204