from enum import StrEnum


class TestStatus(StrEnum):
    __test__ = False

    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    PENDING = "PENDING"