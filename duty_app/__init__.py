"""Application factory for Smart Workforce Scheduler."""

from pathlib import Path
import os

from flask import Flask

from .storage import SchedulerStore
from .web import api


def create_app(database_path=None):
    app = Flask(__name__)
    app.config["DATABASE_PATH"] = database_path or os.getenv(
        "SCHEDULER_DATABASE", str(Path("data") / "scheduler.sqlite3")
    )
    app.extensions["scheduler_store"] = SchedulerStore(app.config["DATABASE_PATH"])
    app.register_blueprint(api)
    return app


app = create_app()
