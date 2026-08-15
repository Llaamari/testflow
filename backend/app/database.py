from pymongo import MongoClient
from pymongo.database import Database


_client: MongoClient | None = None
_database: Database | None = None


def init_database(mongo_uri: str) -> None:
    global _client, _database

    _client = MongoClient(mongo_uri)
    _database = _client.get_default_database()


def get_database() -> Database:
    if _database is None:
        raise RuntimeError("Database has not been initialized.")

    return _database


def create_indexes() -> None:
    database = get_database()

    database["test_suites"].create_index("project_id")

    database["test_runs"].create_index("project_id")
    database["test_runs"].create_index("test_suite_id")
    database["test_runs"].create_index("status")
    database["test_runs"].create_index("started_at")
    database["test_runs"].create_index("software_version")

    database["test_results"].create_index("test_run_id")
    database["test_results"].create_index("status")

    database["test_runs"].create_index(
        "run_id",
        unique=True,
    )