from datetime import UTC, datetime

from bson import ObjectId

from app.repositories.project_repository import ProjectRepository
from app.repositories.test_suite_repository import TestSuiteRepository


class TestSuiteService:
    def __init__(
        self,
        suite_repository: TestSuiteRepository,
        project_repository: ProjectRepository,
    ):
        self.suite_repository = suite_repository
        self.project_repository = project_repository

    def get_suites_for_project(
        self,
        project_id: str,
    ) -> list[dict] | None:
        project = self.project_repository.find_by_id(project_id)

        if project is None:
            return None

        return self.suite_repository.find_by_project_id(project_id)

    def get_suite(self, suite_id: str) -> dict | None:
        return self.suite_repository.find_by_id(suite_id)

    def create_suite(
        self,
        project_id: str,
        name: str,
        description: str,
    ) -> dict | None:
        project = self.project_repository.find_by_id(project_id)

        if project is None:
            return None

        now = datetime.now(UTC)

        suite_data = {
            "project_id": ObjectId(project_id),
            "name": name,
            "description": description,
            "created_at": now,
            "updated_at": now,
        }

        return self.suite_repository.create(suite_data)

    def update_suite(
        self,
        suite_id: str,
        updates: dict,
    ) -> dict | None:
        updates["updated_at"] = datetime.now(UTC)

        return self.suite_repository.update(
            suite_id,
            updates,
        )

    def delete_suite(self, suite_id: str) -> bool:
        return self.suite_repository.delete(suite_id)