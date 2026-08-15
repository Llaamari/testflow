from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.models.status import TestStatus


@dataclass
class TestResult:
    test_run_id: str
    test_name: str
    status: TestStatus
    duration_ms: float
    timestamp: datetime
    error_message: str | None = None
    measurements: dict[str, Any] | None = None