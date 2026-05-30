"""Trend analysis for team performance over time."""
import pandas as pd
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def rolling_win_rate(matches: pd.DataFrame, team: str, window: int = 10) -> pd.Series:
    """Return rolling win rate over a sliding window for a team."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").copy()

    def _won(row):
        is_home = row["homeTeam"] == team
        if is_home:
            return 1 if row["homeScore"] > row["awayScore"] else 0
        return 1 if row["awayScore"] > row["homeScore"] else 0

    team_matches["won"] = team_matches.apply(_won, axis=1)
    return team_matches["won"].rolling(window=window, min_periods=1).mean()


def performance_trend(matches: pd.DataFrame, team: str, window: int = 5) -> str:
    """Return 'improving', 'declining', or 'stable' based on recent win rate trend."""
    rates = rolling_win_rate(matches, team, window).values
    if len(rates) < 2:
        return "stable"
    slope = float(np.polyfit(range(len(rates)), rates, 1)[0])
    if slope > 0.03:
        return "improving"
    elif slope < -0.03:
        return "declining"
    return "stable"


def goals_per_match_trend(matches: pd.DataFrame, team: str, window: int = 5) -> float:
    """Return the slope of goals-per-match over recent games."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").tail(window)

    goals = [
        row["homeScore"] if row["homeTeam"] == team else row["awayScore"]
        for _, row in team_matches.iterrows()
    ]
    if len(goals) < 2:
        return 0.0
    return float(np.polyfit(range(len(goals)), goals, 1)[0])
