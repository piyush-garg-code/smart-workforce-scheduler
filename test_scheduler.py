"""Pytest coverage for scheduling, persistence, and analytics behavior."""

from datetime import date, timedelta

import pytest

from duty_app import create_app
from duty_app.workcalendar import is_business_day, next_business_day


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.sqlite3"))
    app.config["TESTING"] = True
    return app.test_client()


def test_business_day_skips_weekend():
    friday = date(2026, 10, 2)
    assert next_business_day(friday + timedelta(days=1)) == date(2026, 10, 5)
    assert is_business_day(friday)


def test_schedule_generation_and_filtering(client):
    response = client.post("/api/schedules", json={"workers": ["Asha", "Ben"]})
    assert response.status_code == 201
    assert len(response.json["assignments"]) == 16
    response = client.get("/api/schedules?worker=Asha")
    assert response.status_code == 200
    assert all(item["worker"] == "Asha" for item in response.json["assignments"])


def test_invalid_schedule_is_rejected(client):
    response = client.post("/api/schedules", json={"workers": []})
    assert response.status_code == 400


def test_analytics_counts_assignments(client):
    client.post("/api/schedules", json={"workers": ["Asha", "Ben"]})
    response = client.get("/api/analytics")
    assert response.json["total_assignments"] == 16
    assert response.json["assignments_by_worker"] == {"Asha": 8, "Ben": 8}
