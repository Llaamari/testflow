from bson import ObjectId
from pymongo.database import Database


class TestRunRepository:
    def __init__(self, database: Database):
        self.collection = database["test_runs"]

    def find_all(self) -> list[dict]:
        return list(
            self.collection.find().sort("started_at", -1)
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