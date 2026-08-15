from typing import Any


def serialize_document(document: dict[str, Any]) -> dict[str, Any]:
    serialized = document.copy()

    if "_id" in serialized:
        serialized["id"] = str(serialized.pop("_id"))

    return serialized