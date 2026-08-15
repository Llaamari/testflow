import os


class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/testflow",
    )


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True