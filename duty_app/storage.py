"""Small SQLite persistence layer for assignments and time-off records."""

from datetime import date
from pathlib import Path
import sqlite3

from .models import Assignment


class SchedulerStore:
    def __init__(self, database_path):
        self.database_path = database_path
        self._ensure_schema()

    def _connect(self):
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_schema(self):
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS assignments (
                    duty_date TEXT PRIMARY KEY,
                    worker TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS time_off (
                    worker TEXT NOT NULL,
                    duty_date TEXT NOT NULL,
                    PRIMARY KEY (worker, duty_date)
                );
                """
            )

    def replace_assignments(self, assignments):
        with self._connect() as connection:
            connection.execute("DELETE FROM assignments")
            connection.execute("DELETE FROM time_off")
            connection.executemany(
                "INSERT INTO assignments(duty_date, worker) VALUES (?, ?)",
                [(item.duty_date.isoformat(), item.worker) for item in assignments],
            )

    def all_assignments(self):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT duty_date, worker FROM assignments ORDER BY duty_date"
            ).fetchall()
        return [Assignment(date.fromisoformat(row["duty_date"]), row["worker"]) for row in rows]

    def assignment(self, duty_date):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT duty_date, worker FROM assignments WHERE duty_date = ?",
                (duty_date.isoformat(),),
            ).fetchone()
        return None if row is None else Assignment(duty_date, row["worker"])

    def swap(self, first_date, second_date):
        with self._connect() as connection:
            first = connection.execute(
                "SELECT worker FROM assignments WHERE duty_date = ?",
                (first_date.isoformat(),),
            ).fetchone()
            second = connection.execute(
                "SELECT worker FROM assignments WHERE duty_date = ?",
                (second_date.isoformat(),),
            ).fetchone()
            if first is None or second is None:
                return False
            connection.execute(
                "UPDATE assignments SET worker = ? WHERE duty_date = ?",
                (second["worker"], first_date.isoformat()),
            )
            connection.execute(
                "UPDATE assignments SET worker = ? WHERE duty_date = ?",
                (first["worker"], second_date.isoformat()),
            )
            return True

    def mark_time_off(self, worker, duty_date):
        with self._connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO time_off(worker, duty_date) VALUES (?, ?)",
                (worker, duty_date.isoformat()),
            )

    def is_time_off(self, worker, duty_date):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM time_off WHERE worker = ? AND duty_date = ?",
                (worker, duty_date.isoformat()),
            ).fetchone()
        return row is not None
