from datetime import datetime
from typing import Any

from app.models.status import TestStatus


def validate_json_results(
    payload: Any,
) -> tuple[list[dict] | None, list[dict]]:
    errors = []

    if not isinstance(payload, dict):
        return None, [
            {
                "field": None,
                "message": "Request body must be a JSON object.",
            }
        ]

    results = payload.get("results")

    if not isinstance(results, list):
        return None, [
            {
                "field": "results",
                "message": "Results must be an array.",
            }
        ]

    if not results:
        return None, [
            {
                "field": "results",
                "message": "Results array must not be empty.",
            }
        ]

    validated_results = []

    for index, item in enumerate(results):
        row_errors = _validate_result(item, index)

        if row_errors:
            errors.extend(row_errors)
            continue

        validated_results.append(
            _normalize_result(item)
        )

    if errors:
        return None, errors

    return validated_results, []


def _validate_result(
    item: Any,
    index: int,
) -> list[dict]:
    errors = []

    if not isinstance(item, dict):
        return [
            {
                "row": index,
                "field": None,
                "message": "Result must be a JSON object.",
            }
        ]

    test_name = item.get("test_name")

    if not isinstance(test_name, str) or not test_name.strip():
        errors.append(
            {
                "row": index,
                "field": "test_name",
                "message": "Test name is required.",
            }
        )

    status_value = item.get("status")

    try:
        TestStatus(status_value)
    except (ValueError, TypeError):
        errors.append(
            {
                "row": index,
                "field": "status",
                "message": (
                    "Status must be one of: "
                    "PASSED, FAILED, ERROR, PENDING."
                ),
            }
        )

    duration_ms = item.get("duration_ms")

    if (
        not isinstance(duration_ms, (int, float))
        or isinstance(duration_ms, bool)
        or duration_ms < 0
    ):
        errors.append(
            {
                "row": index,
                "field": "duration_ms",
                "message": (
                    "Duration must be a non-negative number."
                ),
            }
        )

    timestamp_value = item.get("timestamp")

    if timestamp_value is not None:
        if not isinstance(timestamp_value, str):
            errors.append(
                {
                    "row": index,
                    "field": "timestamp",
                    "message": (
                        "Timestamp must be an ISO 8601 string."
                    ),
                }
            )
        else:
            try:
                datetime.fromisoformat(
                    timestamp_value.replace("Z", "+00:00")
                )
            except ValueError:
                errors.append(
                    {
                        "row": index,
                        "field": "timestamp",
                        "message": (
                            "Timestamp must be a valid ISO 8601 value."
                        ),
                    }
                )

    error_message = item.get("error_message")

    if (
        error_message is not None
        and not isinstance(error_message, str)
    ):
        errors.append(
            {
                "row": index,
                "field": "error_message",
                "message": "Error message must be a string.",
            }
        )

    measurements = item.get("measurements")

    if measurements is not None and not isinstance(
        measurements,
        dict,
    ):
        errors.append(
            {
                "row": index,
                "field": "measurements",
                "message": "Measurements must be a JSON object.",
            }
        )

    return errors


def _normalize_result(item: dict) -> dict:
    timestamp_value = item.get("timestamp")

    timestamp = None

    if timestamp_value is not None:
        timestamp = datetime.fromisoformat(
            timestamp_value.replace("Z", "+00:00")
        )

    return {
        "test_name": item["test_name"].strip(),
        "status": TestStatus(item["status"]),
        "duration_ms": float(item["duration_ms"]),
        "timestamp": timestamp,
        "error_message": item.get("error_message"),
        "measurements": item.get("measurements"),
    }