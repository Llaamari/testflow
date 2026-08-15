from flask import Blueprint, jsonify, request

from app.database import get_database
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.utils.serialization import serialize_document


projects_bp = Blueprint("projects", __name__)


def get_project_service() -> ProjectService:
    database = get_database()
    repository = ProjectRepository(database)

    return ProjectService(repository)


@projects_bp.get("/projects")
def get_projects():
    service = get_project_service()
    projects = service.get_projects()

    return jsonify(
        [serialize_document(project) for project in projects]
    )


@projects_bp.get("/projects/<project_id>")
def get_project(project_id: str):
    service = get_project_service()
    project = service.get_project(project_id)

    if project is None:
        return jsonify(
            {
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": "Project was not found.",
                }
            }
        ), 404

    return jsonify(serialize_document(project))


@projects_bp.post("/projects")
def create_project():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body must contain valid JSON.",
                }
            }
        ), 400

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Project name is required.",
                }
            }
        ), 400

    description = data.get("description", "")

    if not isinstance(description, str):
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Project description must be a string.",
                }
            }
        ), 400

    service = get_project_service()

    project = service.create_project(
        name=name.strip(),
        description=description.strip(),
    )

    return jsonify(serialize_document(project)), 201