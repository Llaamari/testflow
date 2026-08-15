from flask import Blueprint, jsonify

from app.database import get_database
from app.repositories.project_repository import ProjectRepository
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_run_repository import TestRunRepository
from app.services.dashboard_service import DashboardService
from app.utils.serialization import serialize_document


dashboard_bp = Blueprint("dashboard", __name__)


def get_dashboard_service() -> DashboardService:
    database = get_database()

    return DashboardService(
        ProjectRepository(database),
        TestRunRepository(database),
        TestResultRepository(database),
    )


@dashboard_bp.get("/dashboard/stats")
def get_dashboard_stats():
    service = get_dashboard_service()

    stats = service.get_stats()

    stats["recent_runs"] = [
        serialize_document(run)
        for run in stats["recent_runs"]
    ]

    return jsonify(stats)