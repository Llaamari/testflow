from bson import ObjectId
from pymongo.database import Database


class TestSuiteRepository:
    def __init__(self, database: Database):
        self.collection = database["test_suites"]

    def find_by_project_id(self, project_id: str) -> list[dict]:
        if not ObjectId.is_valid(project_id):
            return []

        return list(
            self.collection.find(
                {"project_id": ObjectId(project_id)}
            ).sort("created_at", -1)
        )

    def find_by_id(self, suite_id: str) -> dict | None:
        if not ObjectId.is_valid(suite_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(suite_id)}
        )

    def create(self, suite_data: dict) -> dict:
        result = self.collection.insert_one(suite_data)

        return self.collection.find_one(
            {"_id": result.inserted_id}
        )

    def update(
        self,
        suite_id: str,
        updates: dict,
    ) -> dict | None:
        if not ObjectId.is_valid(suite_id):
            return None

        object_id = ObjectId(suite_id)

        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": updates},
        )

        if result.matched_count == 0:
            return None

        return self.collection.find_one(
            {"_id": object_id}
        )

    def delete(self, suite_id: str) -> bool:
        if not ObjectId.is_valid(suite_id):
            return False

        result = self.collection.delete_one(
            {"_id": ObjectId(suite_id)}
        )

        return result.deleted_count == 1