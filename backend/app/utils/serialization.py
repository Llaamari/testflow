from enum import Enum
from typing import Any

from bson import ObjectId


def serialize_document(document: dict[str, Any]) -> dict[str, Any]:
    serialized = document.copy()

    if "_id" in serialized:
        serialized["id"] = str(serialized.pop("_id"))

    for key, value in serialized.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, Enum):
            serialized[key] = value.value

    return serialized