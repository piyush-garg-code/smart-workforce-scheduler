"""Business-day calculations without an external calendar dependency."""

from datetime import date, timedelta


def _observed_holidays(year):
    fixed = ((1, 1), (7, 4), (12, 25))
    holidays = set()
    for month, day in fixed:
        holiday = date(year, month, day)
        if holiday.weekday() == 5:
            holidays.add(holiday - timedelta(days=1))
        elif holiday.weekday() == 6:
            holidays.add(holiday + timedelta(days=1))
        else:
            holidays.add(holiday)
    return holidays


def is_business_day(day):
    return day.weekday() < 5 and day not in _observed_holidays(day.year)


def next_business_day(day):
    while not is_business_day(day):
        day += timedelta(days=1)
    return day


def business_days(start, count):
    result = []
    cursor = start
    while len(result) < count:
        cursor = next_business_day(cursor)
        result.append(cursor)
        cursor += timedelta(days=1)
    return result
