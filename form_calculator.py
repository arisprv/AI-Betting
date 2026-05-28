"""Calculate team form from recent match results."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)

POINTS_MAP = {1: 3, 0: 1, -1: 0}


def get_result(home_score: int, away_score: int, perspective: str = "home") -> int:
    if home_score > away_score:
        return 1 if perspective == "home" else -1
    elif home_score == away_score:
        return 0
    return -1 if perspective == "home" else 1


def recent_form_points(matches: pd.DataFrame, team: str, n: int = 5) -> int:
    """Return total points from last n matches for a team."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").tail(n)

    total = 0
    for _, row in team_matches.iterrows():
        perspective = "home" if row["homeTeam"] == team else "away"
        result = get_result(row["homeScore"], row["awayScore"], perspective)
        total += POINTS_MAP[result]
    return total


def form_string(matches: pd.DataFrame, team: str, n: int = 5) -> str:
    """Return a string like 'WWDLW' representing last n results."""
    team_matches = matches[
        (matches["homeTeam"] == team) | (matches["awayTeam"] == team)
    ].sort_values("date").tail(n)

    labels = {1: "W", 0: "D", -1: "L"}
    chars = []
    for _, row in team_matches.iterrows():
        perspective = "home" if row["homeTeam"] == team else "away"
        result = get_result(row["homeScore"], row["awayScore"], perspective)
        chars.append(labels[result])
    return "".join(chars)


def form_points_all_teams(matches: pd.DataFrame, n: int = 5) -> dict[str, int]:
    """Return form points for every team in the matches DataFrame."""
    teams = pd.unique(matches[["homeTeam", "awayTeam"]].values.ravel())
    return {team: recent_form_points(matches, team, n) for team in teams}
