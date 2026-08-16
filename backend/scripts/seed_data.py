import os

from datetime import UTC, datetime, timedelta
from random import Random

from bson import ObjectId

from app.database import get_database, init_database
from app.models.status import TestStatus
from app.services.status_service import aggregate_status


random = Random(42)


PROJECTS = [
    {
        "name": "Autonomous Drone Control System",
        "description": (
            "Fictional control software for autonomous navigation "
            "and telemetry validation."
        ),
        "suites": [
            "Navigation Tests",
            "Sensor Tests",
            "Communication Tests",
        ],
    },
    {
        "name": "Smart Greenhouse Monitoring Platform",
        "description": (
            "Fictional platform for environmental monitoring "
            "and greenhouse automation."
        ),
        "suites": [
            "Climate Control Tests",
            "Sensor Accuracy Tests",
            "Alerting Tests",
        ],
    },
    {
        "name": "Warehouse Robotics Simulator",
        "description": (
            "Fictional software project for warehouse robotics "
            "simulation and route planning."
        ),
        "suites": [
            "Movement Tests",
            "Collision Avoidance Tests",
            "Performance Tests",
        ],
    },
    {
        "name": "Satellite Telemetry Processing Service",
        "description": (
            "Fictional backend service for processing simulated "
            "satellite telemetry."
        ),
        "suites": [
            "Telemetry Parsing Tests",
            "Data Integrity Tests",
            "Resilience Tests",
        ],
    },
]

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/testflow",
)


def reset_database() -> None:
    database = get_database()

    database["test_results"].delete_many({})
    database["test_runs"].delete_many({})
    database["test_suites"].delete_many({})
    database["projects"].delete_many({})


def create_projects() -> list[dict]:
    database = get_database()

    projects = []

    now = datetime.now(UTC)

    for project_data in PROJECTS:
        document = {
            "name": project_data["name"],
            "description": project_data["description"],
            "created_at": now,
            "updated_at": now,
        }

        result = database["projects"].insert_one(
            document
        )

        projects.append(
            {
                "_id": result.inserted_id,
                **project_data,
            }
        )

    return projects


def create_test_suites(
    projects: list[dict],
) -> list[dict]:
    database = get_database()

    suites = []

    now = datetime.now(UTC)

    for project in projects:
        for suite_name in project["suites"]:
            document = {
                "project_id": project["_id"],
                "name": suite_name,
                "description": (
                    f"Fictional automated test suite for "
                    f"{suite_name.lower()}."
                ),
                "created_at": now,
                "updated_at": now,
            }

            result = database["test_suites"].insert_one(
                document
            )

            suites.append(
                {
                    "_id": result.inserted_id,
                    "project_id": project["_id"],
                    "name": suite_name,
                }
            )

    return suites

SOFTWARE_VERSIONS = [
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "2.0.0",
    "2.1.0",
]


def create_test_runs(
    suites: list[dict],
) -> list[dict]:
    database = get_database()

    runs = []

    now = datetime.now(UTC)

    selected_suites = suites[:12]

    for index, suite in enumerate(selected_suites):
        started_at = (
            now
            - timedelta(
                days=index,
                hours=random.randint(0, 8),
            )
        )

        document = {
            "run_id": (
                f"RUN-DEMO-{index + 1:03d}"
            ),
            "project_id": suite["project_id"],
            "test_suite_id": suite["_id"],
            "software_version": (
                SOFTWARE_VERSIONS[
                    index % len(SOFTWARE_VERSIONS)
                ]
            ),
            "status": TestStatus.PENDING.value,
            "started_at": started_at,
            "completed_at": None,
            "created_at": started_at,
        }

        result = database["test_runs"].insert_one(
            document
        )

        runs.append(
            {
                "_id": result.inserted_id,
                **document,
            }
        )

    return runs

TEST_NAMES = [
    "initialization",
    "configuration_validation",
    "connection_recovery",
    "data_processing",
    "input_validation",
    "output_integrity",
    "timeout_handling",
    "resource_cleanup",
    "boundary_conditions",
    "performance_baseline",
    "state_transition",
    "error_recovery",
    "concurrent_operation",
    "serialization",
    "persistence",
]


def generate_status() -> TestStatus:
    value = random.random()

    if value < 0.78:
        return TestStatus.PASSED

    if value < 0.90:
        return TestStatus.FAILED

    if value < 0.96:
        return TestStatus.ERROR

    return TestStatus.PENDING


def create_test_results(
    runs: list[dict],
) -> int:
    database = get_database()

    result_count = 0

    for run_index, run in enumerate(runs):
        statuses = []

        number_of_results = random.randint(
            12,
            18,
        )

        for result_index in range(
            number_of_results
        ):
            status = generate_status()
            statuses.append(status)

            test_name = TEST_NAMES[
                result_index % len(TEST_NAMES)
            ]

            duration_ms = round(
                random.uniform(
                    40.0,
                    1500.0,
                ),
                2,
            )

            timestamp = (
                run["started_at"]
                + timedelta(
                    seconds=result_index * 2,
                )
            )

            error_message = None

            if status == TestStatus.FAILED:
                error_message = (
                    "Observed result did not match "
                    "the expected fictional test condition."
                )

            elif status == TestStatus.ERROR:
                error_message = (
                    "Simulated test execution error."
                )

            measurements = {
                "cpu_percent": round(
                    random.uniform(
                        10.0,
                        75.0,
                    ),
                    1,
                ),
                "memory_mb": round(
                    random.uniform(
                        120.0,
                        640.0,
                    ),
                    1,
                ),
            }

            database["test_results"].insert_one(
                {
                    "test_run_id": run["_id"],
                    "test_name": (
                        f"{test_name}_"
                        f"{run_index + 1:02d}_"
                        f"{result_index + 1:02d}"
                    ),
                    "status": status.value,
                    "duration_ms": duration_ms,
                    "timestamp": timestamp,
                    "error_message": error_message,
                    "measurements": measurements,
                }
            )

            result_count += 1

        aggregated_status = aggregate_status(
            statuses
        )

        completed_at = (
            run["started_at"]
            + timedelta(
                seconds=number_of_results * 2,
            )
        )

        database["test_runs"].update_one(
            {
                "_id": run["_id"],
            },
            {
                "$set": {
                    "status": aggregated_status.value,
                    "completed_at": completed_at,
                }
            },
        )

    return result_count


def main() -> None:
    print("Connecting to TestFlow database...")

    init_database(MONGO_URI)

    print("Clearing existing development data...")
    reset_database()

    print("Creating projects...")
    projects = create_projects()

    print("Creating test suites...")
    suites = create_test_suites(projects)

    print("Creating test runs...")
    runs = create_test_runs(suites)

    print("Creating test results...")
    result_count = create_test_results(runs)

    print()
    print("TestFlow demo data created.")
    print(f"Projects: {len(projects)}")
    print(f"Test suites: {len(suites)}")
    print(f"Test runs: {len(runs)}")
    print(f"Test results: {result_count}")


if __name__ == "__main__":
    main()