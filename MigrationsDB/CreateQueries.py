
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# Project paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SQL_DIR = BASE_DIR / "SqlMigrationFiles"

# Load environment variables from the project root
load_dotenv(PROJECT_ROOT / ".env")

# Execute SQL files in dependency order.
# The filenames do not need to be renumbered.
SQL_FILES = [
    "1_CreateTraveler.sql",
    "2_CreateAgency.sql",
    "9_CreateVisaType.sql",
    "3_CreateTour.sql",
    "11_Cart.sql",
    "7_CreateBooking.sql",
    "5_CreateVisaApplication.sql",
    "8_CreatePayment.sql",
    "4_CreateTourBooking.sql",
    "6_CreateVisaApplicationBooking.sql",
    "10_CartItems.sql",
    "12_CartTriggers.sql",
]


def get_db_connection():
    """Connect to the existing Visitour PostgreSQL database."""
    required_variables = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            "Missing database environment variables: "
            + ", ".join(missing)
        )

    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
    )


def run_migrations():
    """Execute SQL files sequentially, stopping on the first failure."""
    if not SQL_DIR.is_dir():
        raise FileNotFoundError(
            f"SQL directory was not found: {SQL_DIR}"
        )

    connection = None

    try:
        connection = get_db_connection()
        connection.autocommit = False

        print("Connected to the Visitour database.")
        print(f"SQL directory: {SQL_DIR}")

        for filename in SQL_FILES:
            sql_file = SQL_DIR / filename

            if not sql_file.is_file():
                raise FileNotFoundError(
                    f"Required SQL file was not found: {sql_file}"
                )

            sql = sql_file.read_text(encoding="utf-8")

            if not sql.strip():
                print(f"Skipping empty file: {filename}")
                continue

            print(f"\nExecuting: {filename}")

            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)

                connection.commit()
                print(f"SUCCESS: {filename}")

            except Exception:
                connection.rollback()
                print(f"FAILED: {filename}")
                raise

        print("\nAll SQL files executed successfully.")

    except Exception as error:
        print(f"\nMigration stopped: {error}", file=sys.stderr)
        sys.exit(1)
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    run_migrations()
