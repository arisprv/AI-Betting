"""Build a comprehensive profile for a team from historical match data."""
import pandas as pd
from form_calculator import recent_form_points, form_string
from scoring_pattern import high_scoring_rate, average_margin
from momentum_features import unbeaten_streak, winning_streak, goal_trend
from logger import get_logger

log = get_logger(__name__)


def build_team_profile(matches: pd.DataFrame, team: str, window: int = 5) -> dict:
    """Return a dict of key stats for a team from recent matches."""
    return {
        "team": team,
        "form_points": recent_form_points(matches, team, window),
        "form_string": form_string(matches, team, window),
        "unbeaten_streak": unbeaten_streak(matches, team),
        "winning_streak": winning_streak(matches, team),
        "goal_trend": round(goal_trend(matches, team, window), 3),
        "high_scoring_rate": round(high_scoring_rate(matches, team, threshold=2), 3),
        "average_margin": round(average_margin(matches, team), 3),
    }


def compare_teams(matches: pd.DataFrame, home: str, away: str, window: int = 5) -> dict:
    """Side-by-side profile comparison of two teams."""
    home_profile = build_team_profile(matches, home, window)
    away_profile = build_team_profile(matches, away, window)
    return {"home": home_profile, "away": away_profile}


def print_team_profile(profile: dict) -> None:
    team = profile.get("team", "Unknown")
    log.info("=== Team Profile: %s ===", team)
    for k, v in profile.items():
        if k != "team":
            log.info("  %-25s %s", k + ":", v)
