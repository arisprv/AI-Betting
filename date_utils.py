from datetime import datetime, date, timedelta
from typing import Union


DateLike = Union[str, datetime, date]


def to_datetime(d: DateLike) -> datetime:
    if isinstance(d, datetime):
        return d
    if isinstance(d, date):
        return datetime.combine(d, datetime.min.time())
    return datetime.fromisoformat(str(d).replace("Z", "+00:00").rstrip("+00:00"))


def today() -> date:
    return date.today()


def days_until(target: DateLike) -> int:
    target_date = to_datetime(target).date()
    return (target_date - today()).days


def matches_in_next_days(df, date_col: str, n_days: int = 7):
    import pandas as pd
    cutoff = datetime.now() + timedelta(days=n_days)
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    return df[(df[date_col] >= datetime.now()) & (df[date_col] <= cutoff)]


def season_from_date(d: DateLike) -> int:
    """Return the football season year (Aug-May convention)."""
    dt = to_datetime(d)
    return dt.year if dt.month >= 8 else dt.year - 1
