import pytest

from app.models.status import TestStatus
from app.services.status_service import aggregate_status


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        (
            [TestStatus.PASSED],
            TestStatus.PASSED,
        ),
        (
            [TestStatus.PASSED, TestStatus.PASSED],
            TestStatus.PASSED,
        ),
        (
            [TestStatus.PASSED, TestStatus.PENDING],
            TestStatus.PENDING,
        ),
        (
            [TestStatus.PASSED, TestStatus.PENDING, TestStatus.FAILED],
            TestStatus.FAILED,
        ),
        (
            [TestStatus.ERROR, TestStatus.PASSED],
            TestStatus.ERROR,
        ),
        (
            [TestStatus.FAILED, TestStatus.PASSED, TestStatus.PENDING],
            TestStatus.FAILED,
        ),
        (
            [
                TestStatus.PASSED,
                TestStatus.PENDING,
                TestStatus.FAILED,
                TestStatus.ERROR,
            ],
            TestStatus.ERROR,
        ),
    ],
)
def test_aggregates_status_by_priority(statuses, expected):
    assert aggregate_status(statuses) == expected


def test_returns_pending_when_no_results_exist():
    assert aggregate_status([]) == TestStatus.PENDING