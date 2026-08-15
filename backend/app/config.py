import os


class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/testflow",
    )

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv(
        "TEST_MONGO_URI",
        "mongodb://localhost:27017/testflow_test",
    )