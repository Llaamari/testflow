from io import BytesIO

import pandas as pd

from app.models.status import TestStatus
from app.validators.parquet_validator import validate_parquet_results


def dataframe_to_parquet_buffer(
    dataframe: pd.DataFrame,
) -> BytesIO:
    buffer = BytesIO()

    dataframe.to_parquet(
        buffer,
        engine="pyarrow",
        index=False,
    )

    buffer.seek(0)

    return buffer


def test_valid_parquet_results_are_normalized():
    dataframe = pd.DataFrame(
        {
            "test_name": [
                "waypoint_navigation",
                "route_recalculation",
            ],
            "status": [
                "PASSED",
                "FAILED",
            ],
            "duration_ms": [
                120.5,
                300.0,
            ],
            "timestamp": [
                "2026-08-15T18:30:00Z",
                "2026-08-15T18:31:00Z",
            ],
        }
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert errors == []
    assert results is not None
    assert len(results) == 2

    assert results[0]["status"] == TestStatus.PASSED
    assert results[0]["duration_ms"] == 120.5


def test_missing_required_column_returns_error():
    dataframe = pd.DataFrame(
        {
            "test_name": ["test_one"],
            "status": ["PASSED"],
            "timestamp": ["2026-08-15T18:30:00Z"],
        }
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert results is None

    fields = {
        error["field"]
        for error in errors
    }

    assert "duration_ms" in fields


def test_invalid_status_returns_error():
    dataframe = pd.DataFrame(
        {
            "test_name": ["test_one"],
            "status": ["SUCCESS"],
            "duration_ms": [100],
            "timestamp": ["2026-08-15T18:30:00Z"],
        }
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert results is None

    assert any(
        error["field"] == "status"
        for error in errors
    )


def test_negative_duration_returns_error():
    dataframe = pd.DataFrame(
        {
            "test_name": ["test_one"],
            "status": ["PASSED"],
            "duration_ms": [-50],
            "timestamp": ["2026-08-15T18:30:00Z"],
        }
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert results is None

    assert any(
        error["field"] == "duration_ms"
        for error in errors
    )


def test_invalid_timestamp_returns_error():
    dataframe = pd.DataFrame(
        {
            "test_name": ["test_one"],
            "status": ["PASSED"],
            "duration_ms": [100],
            "timestamp": ["not-a-date"],
        }
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert results is None

    assert any(
        error["field"] == "timestamp"
        for error in errors
    )


def test_corrupted_parquet_returns_error():
    buffer = BytesIO(
        b"this is not a parquet file"
    )

    results, errors = validate_parquet_results(buffer)

    assert results is None
    assert len(errors) == 1

    assert (
        errors[0]["message"]
        == "The uploaded file could not be read as Parquet."
    )


def test_empty_parquet_returns_error():
    dataframe = pd.DataFrame(
        columns=[
            "test_name",
            "status",
            "duration_ms",
            "timestamp",
        ]
    )

    buffer = dataframe_to_parquet_buffer(dataframe)

    results, errors = validate_parquet_results(buffer)

    assert results is None
    assert len(errors) == 1