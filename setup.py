"""Create the local SQLite schema used by the scheduler."""

from duty_app import app


if __name__ == "__main__":
    app.extensions["scheduler_store"]._ensure_schema()
    print("Scheduler database is ready.")
