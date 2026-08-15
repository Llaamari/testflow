from bson import ObjectId
from pymongo.database import Database


class ProjectRepository:
    def __init__(self, database: Database):
        self.collection = database["projects"]

    def find_all(self) -> list[dict]:
        return list(
            self.collection.find().sort("created_at", -1)
        )

    def find_by_id(self, project_id: str) -> dict | None:
        if not ObjectId.is_valid(project_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(project_id)}
        )

    def create(self, project_data: dict) -> dict:
        result = self.collection.insert_one(project_data)

        return self.collection.find_one(
            {"_id": result.inserted_id}
        )