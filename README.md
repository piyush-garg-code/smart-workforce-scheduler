# Smart Workforce Scheduler & Analytics Platform

An independently implemented workforce duty scheduler with a small HTTP API,
SQLite persistence, rotation generation, future-date swaps, and assignment
analytics. The current implementation is maintained by Piyush Garg.

## Architecture

- `duty_app/__init__.py` exposes a Flask application factory.
- `duty_app/storage.py` is the persistence boundary and owns the SQLite schema.
- `duty_app/workcalendar.py` provides business-day calculations.
- `duty_app/web.py` contains the HTTP API.
- `cli.py` is a dependency-light command-line client.

The database contains two tables: `assignments` (one worker per duty date) and
`time_off` (worker/date exceptions). SQLite keeps local development simple and
avoids hardcoded credentials.

## Scheduling algorithm

Schedule creation accepts a worker list and optional start date. It generates
eight rotations per worker, skips weekends and observed New Year's Day,
Independence Day, and Christmas, and assigns workers in round-robin order.
Only future assignments may be swapped.

## API

- `GET /` health check
- `POST /api/schedules` with `{"workers": ["Asha", "Ben"]}`
- `GET /api/schedules` or `GET /api/schedules?worker=Asha`
- `POST /api/schedules/swap` with `{"first_date": "...", "second_date": "..."}`
- `GET /api/analytics`

## Installation and usage

Python 3.10+ is recommended.

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python setup.py
python duty_scheduler.py
```

In another terminal:

```text
python cli.py --workers Asha Ben Carlos
python cli.py --analytics
python -m pytest
```

Set `SCHEDULER_DATABASE` to choose another SQLite file. No `.env` file or
credential is required.

## Limitations and future improvements

The holiday list is intentionally small, time-off reassignment is not exposed
yet, and the API has no authentication or multi-tenant isolation. Future work
should add a configurable holiday provider, transactional reassignment rules,
role-based access, richer metrics, and a browser dashboard.

## Acknowledgements / third-party components

This repository was originally started from a Duty Scheduler codebase
associated with `Saykar/Duty-Scheduler`. The earlier repository did not expose
a discoverable license file through its GitHub repository metadata at audit
time. The prior implementation has therefore not been retained as the runtime
implementation; the current code, schema, API, tests, and documentation were
rewritten independently. See [docs/IP_AND_LICENSE_AUDIT.md](docs/IP_AND_LICENSE_AUDIT.md)
for the technical audit and items requiring human review.
