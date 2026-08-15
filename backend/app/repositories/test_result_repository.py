from bson import ObjectId
from pymongo.database import Database


class TestResultRepository:
    def __init__(self, database: Database):
        self.collection = database["test_results"]

    def find_by_test_run_id(self, test_run_id: str) -> list[dict]:
        if not ObjectId.is_valid(test_run_id):
            return []

        return list(
            self.collection.find(
                {"test_run_id": ObjectId(test_run_id)}
            ).sort("timestamp", 1)
        )

    def create(self, result_data: dict) -> dict:
        result = self.collection.insert_one(result_data)

        return self.collection.find_one(
            {"_id": result.inserted_id}
        )