"""Identify teams and match-ups with historically high draw rates."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def team_draw_rate(matches: pd.DataFrame, team: str) -> float:
    """Return draw rate for a specific team."""
    team_matches = matches[(matches["homeTeam"] == team) | (matches["awayTeam"] == team)]
    if team_matches.empty:
        return 0.0
    draws = (team_matches["homeScore"] == team_matches["awayScore"]).sum()
    return draws / len(team_matches)


def top_draw_teams(matches: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return teams with highest draw rates."""
    teams = pd.unique(matches[["homeTeam", "awayTeam"]].values.ravel())
    records = [{"team": t, "draw_rate": team_draw_rate(matches, t)} for t in teams]
    return pd.DataFrame(records).sort_values("draw_rate", ascending=False).head(n).reset_index(drop=True)


def h2h_draw_rate(matches: pd.DataFrame, team_a: str, team_b: str) -> float:
    """Return historical draw rate in head-to-head encounters."""
    h2h = matches[
        ((matches["homeTeam"] == team_a) & (matches["awayTeam"] == team_b)) |
        ((matches["homeTeam"] == team_b) & (matches["awayTeam"] == team_a))
    ]
    if h2h.empty:
        return 0.0
    draws = (h2h["homeScore"] == h2h["awayScore"]).sum()
    return draws / len(h2h)


def draw_probability_indicator(team_a_draw_rate: float, team_b_draw_rate: float,
                                 h2h_draw_rate_val: float, weight: float = 0.4) -> float:
    """Composite draw probability indicator from team and H2H draw rates."""
    return (team_a_draw_rate * (1 - weight) / 2 +
            team_b_draw_rate * (1 - weight) / 2 +
            h2h_draw_rate_val * weight)
