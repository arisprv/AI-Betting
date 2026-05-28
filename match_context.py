"""Contextual match features: rivalry, derby, cup pressure, fatigue."""
import pandas as pd
from datetime import timedelta
from logger import get_logger

log = get_logger(__name__)


def days_since_last_match(matches: pd.DataFrame, team: str, before_date) -> int:
    """Return days since a team's most recent match, or 7 if none found."""
    team_matches = matches[
        ((matches["homeTeam"] == team) | (matches["awayTeam"] == team)) &
        (matches["date"] < before_date)
    ].sort_values("date")

    if team_matches.empty:
        return 7

    last_date = pd.to_datetime(team_matches["date"].iloc[-1])
    before = pd.to_datetime(before_date)
    return (before - last_date).days


def is_high_rest_advantage(home_days: int, away_days: int, threshold: int = 3) -> bool:
    """Return True if one team has significantly more rest."""
    return abs(home_days - away_days) >= threshold


def matches_in_last_n_days(matches: pd.DataFrame, team: str, before_date, n: int = 14) -> int:
    """Count how many matches a team played in the last n days (fixture congestion)."""
    cutoff = pd.to_datetime(before_date) - timedelta(days=n)
    before = pd.to_datetime(before_date)
    team_matches = matches[
        ((matches["homeTeam"] == team) | (matches["awayTeam"] == team)) &
        (pd.to_datetime(matches["date"]) >= cutoff) &
        (pd.to_datetime(matches["date"]) < before)
    ]
    return len(team_matches)


def fatigue_index(matches_count: int, days_of_rest: int) -> float:
    """Simple fatigue score: more matches + less rest = higher fatigue."""
    return matches_count / max(days_of_rest, 1)
