"""Typed records used by the scheduler service."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Assignment:
    duty_date: date
    worker: str


@dataclass(frozen=True)
class TimeOff:
    worker: str
    duty_date: date
