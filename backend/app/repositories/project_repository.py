from pymongo.database import Database


class ProjectRepository:
    def __init__(self, database: Database):
        self.collection = database["projects"]