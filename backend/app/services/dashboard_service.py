from app.repositories.project_repository import ProjectRepository
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository


class DashboardService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        run_repository: TestRunRepository,
        result_repository: TestResultRepository,
    ):
        self.project_repository = project_repository
        self.run_repository = run_repository
        self.result_repository = result_repository

    def get_stats(self) -> dict:
        project_count = self.project_repository.count()
        run_count = self.run_repository.count()
        result_count = self.result_repository.count()

        status_distribution = (
            self.result_repository.count_by_status()
        )

        passed = status_distribution["PASSED"]
        failed = status_distribution["FAILED"]
        errors = status_distribution["ERROR"]
        pending = status_distribution["PENDING"]

        completed_results = (
            passed
            + failed
            + errors
        )

        pass_rate = 0.0

        if completed_results > 0:
            pass_rate = round(
                passed / completed_results * 100,
                1,
            )

        recent_runs = self.run_repository.find_recent(
            limit=5
        )

        return {
            "projects": project_count,
            "test_runs": run_count,
            "test_results": result_count,
            "pass_rate": pass_rate,
            "failed": failed,
            "errors": errors,
            "pending": pending,
            "status_distribution": status_distribution,
            "recent_runs": recent_runs,
        }