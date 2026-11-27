
import sqlite3
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DB_PATH = BASE_DIR / "college_management.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DB_PATH)

    # Enable foreign key enforcement for this connection
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
