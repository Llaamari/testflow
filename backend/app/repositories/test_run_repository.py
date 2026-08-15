from bson import ObjectId
from datetime import datetime

from bson import ObjectId
from pymongo.database import Database


class TestRunRepository:
    def __init__(self, database: Database):
        self.collection = database["test_runs"]

    def find_all(
        self,
        project_id: str | None = None,
        status: str | None = None,
        software_version: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict]:
        query = {}

        if project_id is not None:
            if not ObjectId.is_valid(project_id):
                return []

            query["project_id"] = ObjectId(project_id)

        if status is not None:
            query["status"] = status

        if software_version is not None:
            query["software_version"] = software_version

        if date_from is not None or date_to is not None:
            started_at_query = {}

            if date_from is not None:
                started_at_query["$gte"] = date_from

            if date_to is not None:
                started_at_query["$lte"] = date_to

            query["started_at"] = started_at_query

        return list(
            self.collection.find(query).sort("started_at", -1)
        )

    def find_by_id(self, run_id: str) -> dict | None:
        if not ObjectId.is_valid(run_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(run_id)}
        )

    def create(self, run_data: dict) -> dict:
        result = self.collection.insert_one(run_data)

        return self.collection.find_one(
            {"_id": result.inserted_id}
        )

    def delete(self, run_id: str) -> bool:
        if not ObjectId.is_valid(run_id):
            return False

        result = self.collection.delete_one(
            {"_id": ObjectId(run_id)}
        )

        return result.deleted_count == 1

    def update_status(
        self,
        test_run_id: str,
        status: str,
    ) -> dict | None:
        if not ObjectId.is_valid(test_run_id):
            return None

        object_id = ObjectId(test_run_id)

        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": {"status": status}},
        )

        if result.matched_count == 0:
            return None

        return self.collection.find_one(
            {"_id": object_id}
        )