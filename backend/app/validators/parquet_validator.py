from io import BytesIO
from typing import BinaryIO

import pandas as pd

from app.models.status import TestStatus


REQUIRED_COLUMNS = {
    "test_name",
    "status",
    "duration_ms",
    "timestamp",
}

OPTIONAL_COLUMNS = {
    "error_message",
}

def validate_parquet_results(
    file: BinaryIO,
) -> tuple[list[dict] | None, list[dict]]:
    try:
        file_content = file.read()

        dataframe = pd.read_parquet(
            BytesIO(file_content),
            engine="pyarrow",
        )
    except Exception:
        return None, [
            {
                "field": None,
                "message": "The uploaded file could not be read as Parquet.",
            }
        ]

    column_errors = _validate_columns(dataframe)

    if column_errors:
        return None, column_errors

    if dataframe.empty:
        return None, [
            {
                "field": None,
                "message": "Parquet file must contain at least one result.",
            }
        ]

    normalized_results, errors = _validate_rows(dataframe)

    if errors:
        return None, errors

    return normalized_results, []

def _validate_columns(
    dataframe: pd.DataFrame,
) -> list[dict]:
    columns = set(dataframe.columns)

    missing_columns = REQUIRED_COLUMNS - columns

    if not missing_columns:
        return []

    return [
        {
            "field": column,
            "message": f"Required column '{column}' is missing.",
        }
        for column in sorted(missing_columns)
    ]

def _validate_rows(
    dataframe: pd.DataFrame,
) -> tuple[list[dict], list[dict]]:
    normalized_results = []
    errors = []

    for index, row in dataframe.iterrows():
        result, row_errors = _validate_row(
            row,
            int(index),
        )

        if row_errors:
            errors.extend(row_errors)
        else:
            normalized_results.append(result)

    return normalized_results, errors

def _validate_row(
    row: pd.Series,
    index: int,
) -> tuple[dict | None, list[dict]]:
    errors = []

    test_name = row["test_name"]

    if pd.isna(test_name) or not str(test_name).strip():
        errors.append(
            {
                "row": index,
                "field": "test_name",
                "message": "Test name is required.",
            }
        )

    status_value = row["status"]

    try:
        status = TestStatus(str(status_value))
    except ValueError:
        status = None

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

    duration_value = row["duration_ms"]

    try:
        duration_ms = float(duration_value)

        if pd.isna(duration_ms) or duration_ms < 0:
            raise ValueError
    except (TypeError, ValueError):
        duration_ms = None

        errors.append(
            {
                "row": index,
                "field": "duration_ms",
                "message": (
                    "Duration must be a non-negative number."
                ),
            }
        )

    timestamp_value = row["timestamp"]

    try:
        timestamp = pd.to_datetime(
            timestamp_value,
            utc=True,
            errors="raise",
        ).to_pydatetime()
    except (ValueError, TypeError):
        timestamp = None

        errors.append(
            {
                "row": index,
                "field": "timestamp",
                "message": "Timestamp must be a valid datetime value.",
            }
        )

    error_message = None

    if "error_message" in row.index:
        value = row["error_message"]

        if not pd.isna(value):
            if not isinstance(value, str):
                errors.append(
                    {
                        "row": index,
                        "field": "error_message",
                        "message": (
                            "Error message must be a string."
                        ),
                    }
                )
            else:
                error_message = value

    if errors:
        return None, errors

    return {
        "test_name": str(test_name).strip(),
        "status": status,
        "duration_ms": duration_ms,
        "timestamp": timestamp,
        "error_message": error_message,
        "measurements": None,
    }, []