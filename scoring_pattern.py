"""Analyse team scoring patterns — first goal time, late goals, scoring minutes."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def first_goal_rate(matches: pd.DataFrame, team: str) -> float:
    """Return the proportion of matches where team scores first (home only as proxy)."""
    home = matches[matches["homeTeam"] == team]
    if home.empty:
        return 0.0
    scored_first = home[home["homeScore"] > 0]
    return len(scored_first) / len(home)


def high_scoring_rate(matches: pd.DataFrame, team: str, threshold: int = 2) -> float:
    """Proportion of matches where team scored >= threshold goals."""
    team_matches = matches[(matches["homeTeam"] == team) | (matches["awayTeam"] == team)]
    if team_matches.empty:
        return 0.0
    count = 0
    for _, row in team_matches.iterrows():
        gf = row["homeScore"] if row["homeTeam"] == team else row["awayScore"]
        if gf >= threshold:
            count += 1
    return count / len(team_matches)


def average_margin(matches: pd.DataFrame, team: str) -> float:
    """Average goal margin (positive when winning) across all matches."""
    team_matches = matches[(matches["homeTeam"] == team) | (matches["awayTeam"] == team)]
    if team_matches.empty:
        return 0.0
    margins = []
    for _, row in team_matches.iterrows():
        gf = row["homeScore"] if row["homeTeam"] == team else row["awayScore"]
        ga = row["awayScore"] if row["homeTeam"] == team else row["homeScore"]
        margins.append(gf - ga)
    return sum(margins) / len(margins)
