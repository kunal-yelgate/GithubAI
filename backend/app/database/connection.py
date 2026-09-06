import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "analyzer.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS repository_analyses (
            full_name TEXT PRIMARY KEY,
            source_version TEXT,
            analyzed_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    connection.commit()
    return connection