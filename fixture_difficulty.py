"""Fixture difficulty ratings based on opponent Elo or league position."""
import pandas as pd
from elo_ratings import build_elo_ratings, DEFAULT_RATING
from position_tracker import build_table, get_position
from logger import get_logger

log = get_logger(__name__)


def difficulty_by_elo(matches: pd.DataFrame, team: str, upcoming: pd.DataFrame) -> pd.DataFrame:
    """Attach Elo-based difficulty score to each upcoming fixture."""
    ratings = build_elo_ratings(matches)
    rows = []
    for _, row in upcoming[upcoming["homeTeam"] == team].iterrows():
        opp = row["awayTeam"]
        rows.append({"date": row["utcDate"], "opponent": opp, "venue": "H",
                     "opp_elo": ratings.get(opp, DEFAULT_RATING)})
    for _, row in upcoming[upcoming["awayTeam"] == team].iterrows():
        opp = row["homeTeam"]
        rows.append({"date": row["utcDate"], "opponent": opp, "venue": "A",
                     "opp_elo": ratings.get(opp, DEFAULT_RATING)})
    df = pd.DataFrame(rows)
    if not df.empty:
        df["difficulty"] = (df["opp_elo"] - DEFAULT_RATING) / 100
    return df.sort_values("date")


def difficulty_by_position(matches: pd.DataFrame, upcoming: pd.DataFrame, team: str) -> pd.DataFrame:
    """Attach league-position-based difficulty to upcoming fixtures."""
    table = build_table(matches)
    rows = []
    for _, row in upcoming[
        (upcoming["homeTeam"] == team) | (upcoming["awayTeam"] == team)
    ].iterrows():
        opp = row["awayTeam"] if row["homeTeam"] == team else row["homeTeam"]
        pos = get_position(table, opp)
        venue = "H" if row["homeTeam"] == team else "A"
        rows.append({"date": row["utcDate"], "opponent": opp, "venue": venue, "opp_position": pos})
    return pd.DataFrame(rows).sort_values("date")


def average_difficulty(df: pd.DataFrame, col: str = "opp_elo") -> float:
    """Average difficulty score from a fixture difficulty DataFrame."""
    if df.empty or col not in df:
        return 0.0
    return float(df[col].mean())
