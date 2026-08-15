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

    def create_many(
        self,
        results_data: list[dict],
    ) -> list[dict]:
        if not results_data:
            return []

        result = self.collection.insert_many(results_data)

        return list(
            self.collection.find(
                {"_id": {"$in": result.inserted_ids}}
            )
        )

    def count(self) -> int:
        return self.collection.count_documents({})


    def count_by_status(self) -> dict[str, int]:
        statuses = {
            "PASSED": 0,
            "FAILED": 0,
            "ERROR": 0,
            "PENDING": 0,
        }

        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                }
            }
        ]

        for item in self.collection.aggregate(pipeline):
            status = item["_id"]

            if status in statuses:
                statuses[status] = item["count"]

        return statuses