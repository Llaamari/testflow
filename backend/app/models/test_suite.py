from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestSuite:
    project_id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime