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