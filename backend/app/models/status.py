from enum import StrEnum


class TestStatus(StrEnum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    PENDING = "PENDING"