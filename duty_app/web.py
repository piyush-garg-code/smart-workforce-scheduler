"""HTTP API for workforce scheduling and lightweight analytics."""

from datetime import date, datetime

from flask import Blueprint, current_app, jsonify, request

from .models import Assignment
from .workcalendar import business_days

api = Blueprint("api", __name__)


def _store():
    return current_app.extensions["scheduler_store"]


def _parse_day(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


@api.get("/")
def health():
    return jsonify({"service": "Smart Workforce Scheduler & Analytics Platform", "status": "ok"})


@api.post("/api/schedules")
def create_schedule():
    payload = request.get_json(silent=True) or {}
    workers = [str(item).strip() for item in payload.get("workers", []) if str(item).strip()]
    if not workers:
        return jsonify({"error": "workers must contain at least one name"}), 400
    start = _parse_day(payload.get("start_date", date.today().isoformat()))
    assignments = [
        Assignment(day, workers[index % len(workers)])
        for index, day in enumerate(business_days(start, len(workers) * 8))
    ]
    _store().replace_assignments(assignments)
    return jsonify({"assignments": _serialize(assignments)}), 201


@api.get("/api/schedules")
def list_schedules():
    assignments = _store().all_assignments()
    worker = request.args.get("worker")
    if worker:
        assignments = [item for item in assignments if item.worker == worker]
    return jsonify({"assignments": _serialize(assignments)})


@api.post("/api/schedules/swap")
def swap_schedules():
    payload = request.get_json(silent=True) or {}
    try:
        first = _parse_day(payload["first_date"])
        second = _parse_day(payload["second_date"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "first_date and second_date must use YYYY-MM-DD"}), 400
    if first <= date.today() or second <= date.today():
        return jsonify({"error": "only future assignments can be changed"}), 400
    if not _store().swap(first, second):
        return jsonify({"error": "both dates must have assignments"}), 404
    return jsonify({"assignments": _serialize([_store().assignment(first), _store().assignment(second)])})


@api.get("/api/analytics")
def analytics():
    assignments = _store().all_assignments()
    totals = {}
    for item in assignments:
        totals[item.worker] = totals.get(item.worker, 0) + 1
    return jsonify({"total_assignments": len(assignments), "assignments_by_worker": totals})


def _serialize(assignments):
    return [{"date": item.duty_date.isoformat(), "worker": item.worker} for item in assignments]
