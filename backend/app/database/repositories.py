import json
from datetime import datetime, timezone

from app.database.connection import get_connection


def get_cached_analysis(full_name: str, source_version: str | None):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM repository_analyses WHERE full_name = ?",
        (full_name,)
    ).fetchone()
    connection.close()

    if not row or row["source_version"] != source_version:
        return None

    return json.loads(row["payload"])


def save_analysis(full_name: str, source_version: str | None, payload: dict):
    analyzed_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO repository_analyses (full_name, source_version, analyzed_at, payload)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(full_name) DO UPDATE SET
            source_version = excluded.source_version,
            analyzed_at = excluded.analyzed_at,
            payload = excluded.payload
        """,
        (full_name, source_version, analyzed_at, json.dumps(payload))
    )
    connection.commit()
    connection.close()


def list_cached_analyses():
    connection = get_connection()
    rows = connection.execute(
        "SELECT payload FROM repository_analyses ORDER BY analyzed_at DESC"
    ).fetchall()
    connection.close()
    return [json.loads(row["payload"]) for row in rows]