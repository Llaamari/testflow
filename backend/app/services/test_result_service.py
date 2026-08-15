from datetime import UTC, datetime

from bson import ObjectId

from app.models.status import TestStatus
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository
from app.services.status_service import aggregate_status


class TestResultService:
    def __init__(
        self,
        result_repository: TestResultRepository,
        run_repository: TestRunRepository,
    ):
        self.result_repository = result_repository
        self.run_repository = run_repository

    def get_results(
        self,
        test_run_id: str,
    ) -> list[dict] | None:
        run = self.run_repository.find_by_id(test_run_id)

        if run is None:
            return None

        return self.result_repository.find_by_test_run_id(
            test_run_id
        )

    def create_result(
        self,
        test_run_id: str,
        test_name: str,
        status: TestStatus,
        duration_ms: float,
        timestamp: datetime | None = None,
        error_message: str | None = None,
        measurements: dict | None = None,
    ) -> dict | None:
        run = self.run_repository.find_by_id(test_run_id)

        if run is None:
            return None

        result_data = {
            "test_run_id": ObjectId(test_run_id),
            "test_name": test_name,
            "status": status,
            "duration_ms": duration_ms,
            "timestamp": timestamp or datetime.now(UTC),
            "error_message": error_message,
            "measurements": measurements,
        }

        created = self.result_repository.create(result_data)

        self._recalculate_run_status(test_run_id)

        return created

    def _recalculate_run_status(
        self,
        test_run_id: str,
    ) -> None:
        results = self.result_repository.find_by_test_run_id(
            test_run_id
        )

        statuses = [
            TestStatus(result["status"])
            for result in results
        ]

        aggregated_status = aggregate_status(statuses)

        self.run_repository.update_status(
            test_run_id,
            aggregated_status.value,
        )