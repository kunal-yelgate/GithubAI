import os
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "analyzer.db"


class _PostgresCursorProxy:
    def __init__(self, cursor):
        self._cursor = cursor

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        if isinstance(row, dict):
            return row
        return dict(row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        if not rows:
            return []
        return [dict(row) for row in rows]

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class _PostgresConnection:
    def __init__(self, connection):
        self._connection = connection

    def execute(self, query, params=None):
        cursor = self._connection.cursor(row_factory=None)
        cursor.execute(query, params or ())
        return _PostgresCursorProxy(cursor)

    def executemany(self, query, params_seq):
        with self._connection.cursor() as cursor:
            cursor.executemany(query, params_seq)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


def _sqlite_connection():
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
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS code_chunks (
            repository TEXT NOT NULL,
            source_version TEXT,
            file_path TEXT NOT NULL,
            language TEXT,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT,
            PRIMARY KEY (repository, file_path, chunk_index)
        )
        """
    )
    connection.commit()
    return connection


def get_connection():
    database_url = (os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE") or "").strip()

    if database_url:
        try:
            import psycopg
            from psycopg.rows import dict_row

            connection = psycopg.connect(database_url, autocommit=False)
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS repository_analyses (
                        full_name TEXT PRIMARY KEY,
                        source_version TEXT,
                        analyzed_at TEXT NOT NULL,
                        payload JSONB NOT NULL
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS code_chunks (
                        repository TEXT NOT NULL,
                        source_version TEXT,
                        file_path TEXT NOT NULL,
                        language TEXT,
                        chunk_index INTEGER NOT NULL,
                        content TEXT NOT NULL,
                        embedding TEXT,
                        PRIMARY KEY (repository, file_path, chunk_index)
                    )
                    """
                )
            connection.commit()
            return _PostgresConnection(connection)
        except Exception:
            return _sqlite_connection()

    return _sqlite_connection()