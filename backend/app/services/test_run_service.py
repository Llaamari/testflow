from datetime import UTC, datetime

from bson import ObjectId

from app.models.status import TestStatus
from app.repositories.project_repository import ProjectRepository
from app.repositories.test_run_repository import TestRunRepository
from app.repositories.test_suite_repository import TestSuiteRepository


class TestRunService:
    def __init__(
        self,
        run_repository: TestRunRepository,
        project_repository: ProjectRepository,
        suite_repository: TestSuiteRepository,
    ):
        self.run_repository = run_repository
        self.project_repository = project_repository
        self.suite_repository = suite_repository

    def get_runs(
        self,
        project_id: str | None = None,
        status: str | None = None,
        software_version: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict]:
        return self.run_repository.find_all(
            project_id=project_id,
            status=status,
            software_version=software_version,
            date_from=date_from,
            date_to=date_to,
        )

    def get_run(self, test_run_id: str) -> dict | None:
        return self.run_repository.find_by_id(test_run_id)

    def create_run(
        self,
        project_id: str,
        test_suite_id: str,
        software_version: str,
    ) -> dict | None:
        project = self.project_repository.find_by_id(project_id)

        if project is None:
            return None

        suite = self.suite_repository.find_by_id(test_suite_id)

        if suite is None:
            return None

        if str(suite["project_id"]) != project_id:
            return None

        now = datetime.now(UTC)

        run_data = {
            "run_id": self._generate_run_id(now),
            "project_id": ObjectId(project_id),
            "test_suite_id": ObjectId(test_suite_id),
            "software_version": software_version,
            "status": TestStatus.PENDING,
            "started_at": now,
            "completed_at": None,
            "created_at": now,
        }

        return self.run_repository.create(run_data)

    def delete_run(self, test_run_id: str) -> bool:
        return self.run_repository.delete(test_run_id)

    @staticmethod
    def _generate_run_id(timestamp: datetime) -> str:
        return f"RUN-{timestamp:%Y%m%d%H%M%S%f}"