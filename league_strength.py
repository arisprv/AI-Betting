"""Estimate relative league strength using average goals and competitive balance."""
import pandas as pd
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def goals_per_match_by_league(matches: pd.DataFrame) -> pd.Series:
    """Average goals per match, higher = more open/attacking league."""
    matches = matches.copy()
    matches["total_goals"] = matches["homeScore"] + matches["awayScore"]
    return matches.groupby("league")["total_goals"].mean().rename("avg_goals_per_match")


def competitive_balance(matches: pd.DataFrame) -> pd.Series:
    """
    Competitive balance index: standard deviation of results per league.
    Higher = more unpredictable (less dominant teams).
    """
    def _balance(group):
        results = (group["homeScore"] > group["awayScore"]).astype(int)
        return results.std()
    return matches.groupby("league").apply(_balance).rename("competitive_balance")


def home_advantage_by_league(matches: pd.DataFrame) -> pd.Series:
    """Home win rate per league."""
    matches = matches.copy()
    matches["home_win"] = (matches["homeScore"] > matches["awayScore"]).astype(int)
    return matches.groupby("league")["home_win"].mean().rename("home_win_rate")


def league_strength_report(matches: pd.DataFrame) -> pd.DataFrame:
    """Combine multiple metrics into a league strength summary table."""
    gpm = goals_per_match_by_league(matches)
    cb = competitive_balance(matches)
    ha = home_advantage_by_league(matches)
    return pd.concat([gpm, cb, ha], axis=1).reset_index()
