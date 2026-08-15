from flask import Blueprint, jsonify, request

from app.database import get_database
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository
from app.services.import_service import ImportService
from app.validators.json_validator import validate_json_results
from app.validators.parquet_validator import validate_parquet_results


imports_bp = Blueprint("imports", __name__)


def get_import_service() -> ImportService:
    database = get_database()

    return ImportService(
        TestResultRepository(database),
        TestRunRepository(database),
    )

@imports_bp.post(
    "/test-runs/<test_run_id>/results/import/json"
)
def import_json_results(test_run_id: str):
    payload = request.get_json(silent=True)

    results, errors = validate_json_results(payload)

    if errors:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_IMPORT_DATA",
                    "message": (
                        "The JSON test result data "
                        "contains validation errors."
                    ),
                    "details": errors,
                }
            }
        ), 422

    service = get_import_service()

    summary = service.import_results(
        test_run_id,
        results,
    )

    if summary is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return jsonify(
        {
            "imported_count": summary["imported_count"],
            "run_status": summary["status"].value,
        }
    ), 201

@imports_bp.post(
    "/test-runs/<test_run_id>/results/import/parquet"
)
def import_parquet_results(test_run_id: str):
    uploaded_file = request.files.get("file")

    if uploaded_file is None:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_FILE_UPLOAD",
                    "message": "Parquet file is required.",
                }
            }
        ), 400

    if not uploaded_file.filename:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_FILE_UPLOAD",
                    "message": "Uploaded file must have a filename.",
                }
            }
        ), 400

    results, errors = validate_parquet_results(
        uploaded_file.stream
    )

    if errors:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_IMPORT_DATA",
                    "message": (
                        "The Parquet test result file "
                        "contains validation errors."
                    ),
                    "details": errors,
                }
            }
        ), 422

    service = get_import_service()

    summary = service.import_results(
        test_run_id,
        results,
    )

    if summary is None:
        return jsonify(
            {
                "error": {
                    "code": "TEST_RUN_NOT_FOUND",
                    "message": "Test run was not found.",
                }
            }
        ), 404

    return jsonify(
        {
            "imported_count": summary["imported_count"],
            "run_status": summary["status"].value,
        }
    ), 201