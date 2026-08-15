from datetime import UTC, datetime

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_projects(self) -> list[dict]:
        return self.repository.find_all()

    def get_project(self, project_id: str) -> dict | None:
        return self.repository.find_by_id(project_id)

    def create_project(
        self,
        name: str,
        description: str,
    ) -> dict:
        now = datetime.now(UTC)

        project_data = {
            "name": name,
            "description": description,
            "created_at": now,
            "updated_at": now,
        }

        return self.repository.create(project_data)

    def update_project(
        self,
        project_id: str,
        updates: dict,
    ) -> dict | None:
        updates["updated_at"] = datetime.now(UTC)

        return self.repository.update(
            project_id,
            updates,
        )

    def delete_project(self, project_id: str) -> bool:
        return self.repository.delete(project_id)