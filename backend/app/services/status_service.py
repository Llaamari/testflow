from collections.abc import Iterable

from app.models.status import TestStatus


_STATUS_PRIORITY = {
    TestStatus.PASSED: 0,
    TestStatus.PENDING: 1,
    TestStatus.FAILED: 2,
    TestStatus.ERROR: 3,
}


def aggregate_status(statuses: Iterable[TestStatus]) -> TestStatus:
    status_list = list(statuses)

    if not status_list:
        return TestStatus.PENDING

    return max(status_list, key=_STATUS_PRIORITY.get)