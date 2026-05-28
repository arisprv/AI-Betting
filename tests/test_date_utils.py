from datetime import datetime, date
import pytest
from date_utils import to_datetime, season_from_date, days_until


def test_to_datetime_from_str():
    dt = to_datetime("2025-03-15")
    assert dt.year == 2025 and dt.month == 3 and dt.day == 15


def test_to_datetime_from_datetime():
    dt = datetime(2025, 6, 1)
    assert to_datetime(dt) == dt


def test_to_datetime_from_date():
    d = date(2025, 9, 1)
    result = to_datetime(d)
    assert result.year == 2025


def test_season_summer():
    assert season_from_date("2025-09-01") == 2025


def test_season_spring():
    assert season_from_date("2025-03-01") == 2024


def test_season_august_boundary():
    assert season_from_date("2025-08-01") == 2025


def test_days_until_future():
    future = (date.today().replace(year=date.today().year + 1)).isoformat()
    assert days_until(future) > 0
