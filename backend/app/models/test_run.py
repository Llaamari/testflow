from dataclasses import dataclass
from datetime import datetime

from app.models.status import TestStatus


@dataclass
class TestRun:
    run_id: str
    project_id: str
    test_suite_id: str
    software_version: str
    status: TestStatus
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime