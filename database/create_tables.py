
from database.db_connection import get_connection
from pathlib import Path


def create_tables():
    """Execute the SQL schema and create database tables."""

    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    connection = get_connection()

    try:
        connection.executescript(schema)
        connection.commit()
        print("Database tables created successfully!")

    except Exception as error:
        connection.rollback()
        print("Error creating tables:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
