from datetime import UTC, datetime

from bson import ObjectId

from app.models.status import TestStatus
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository
from app.services.status_service import aggregate_status


class ImportService:
    def __init__(
        self,
        result_repository: TestResultRepository,
        run_repository: TestRunRepository,
    ):
        self.result_repository = result_repository
        self.run_repository = run_repository

    def import_results(
        self,
        test_run_id: str,
        results: list[dict],
    ) -> dict | None:
        run = self.run_repository.find_by_id(test_run_id)

        if run is None:
            return None

        documents = []

        for result in results:
            documents.append(
                {
                    "test_run_id": ObjectId(test_run_id),
                    "test_name": result["test_name"],
                    "status": result["status"].value,
                    "duration_ms": result["duration_ms"],
                    "timestamp": (
                        result["timestamp"]
                        or datetime.now(UTC)
                    ),
                    "error_message": result["error_message"],
                    "measurements": result["measurements"],
                }
            )

        created = self.result_repository.create_many(
            documents
        )

        all_results = (
            self.result_repository.find_by_test_run_id(
                test_run_id
            )
        )

        statuses = [
            TestStatus(result["status"])
            for result in all_results
        ]

        aggregated_status = aggregate_status(statuses)

        self.run_repository.update_status(
            test_run_id,
            aggregated_status.value,
        )

        return {
            "imported_count": len(created),
            "status": aggregated_status,
        }