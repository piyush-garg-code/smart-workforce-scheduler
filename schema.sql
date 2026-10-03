-- Persistent schema for Smart Workforce Scheduler.

CREATE TABLE IF NOT EXISTS assignments (
    duty_date TEXT PRIMARY KEY,
    worker TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS time_off (
    worker TEXT NOT NULL,
    duty_date TEXT NOT NULL,
    PRIMARY KEY (worker, duty_date)
);

CREATE INDEX IF NOT EXISTS idx_assignments_worker
    ON assignments(worker);

CREATE INDEX IF NOT EXISTS idx_time_off_date
    ON time_off(duty_date);
