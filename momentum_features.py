"""Advanced momentum and trend features for football team analysis."""
import pandas as pd
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def goal_trend(matches: pd.DataFrame, team: str, window: int = 5) -> float:
    """Return the slope of goals scored over recent matches (positive = improving)."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").tail(window)

    if len(team_matches) < 2:
        return 0.0

    goals = [
        row["homeScore"] if row["homeTeam"] == team else row["awayScore"]
        for _, row in team_matches.iterrows()
    ]
    x = np.arange(len(goals))
    slope, _ = np.polyfit(x, goals, 1)
    return float(slope)


def conceded_trend(matches: pd.DataFrame, team: str, window: int = 5) -> float:
    """Slope of goals conceded (negative is better — team tightening up)."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").tail(window)

    if len(team_matches) < 2:
        return 0.0

    conceded = [
        row["awayScore"] if row["homeTeam"] == team else row["homeScore"]
        for _, row in team_matches.iterrows()
    ]
    x = np.arange(len(conceded))
    slope, _ = np.polyfit(x, conceded, 1)
    return float(slope)


def unbeaten_streak(matches: pd.DataFrame, team: str) -> int:
    """Return current unbeaten streak (W or D) for a team."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date")

    streak = 0
    for _, row in team_matches.iloc[::-1].iterrows():
        hs, as_ = row["homeScore"], row["awayScore"]
        is_home = row["homeTeam"] == team
        if (is_home and hs >= as_) or (not is_home and as_ >= hs):
            streak += 1
        else:
            break
    return streak


def winning_streak(matches: pd.DataFrame, team: str) -> int:
    """Return current winning streak for a team."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date")

    streak = 0
    for _, row in team_matches.iloc[::-1].iterrows():
        hs, as_ = row["homeScore"], row["awayScore"]
        is_home = row["homeTeam"] == team
        if (is_home and hs > as_) or (not is_home and as_ > hs):
            streak += 1
        else:
            break
    return streak
