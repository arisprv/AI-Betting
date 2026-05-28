"""Compute league table standings from match results."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def build_table(matches: pd.DataFrame) -> pd.DataFrame:
    """Compute full league table from match results."""
    records = {}

    def _ensure(team):
        if team not in records:
            records[team] = {"team": team, "played": 0, "won": 0, "drawn": 0, "lost": 0,
                             "gf": 0, "ga": 0, "gd": 0, "points": 0}

    for _, row in matches.iterrows():
        home, away = row["homeTeam"], row["awayTeam"]
        hs, as_ = row["homeScore"], row["awayScore"]
        _ensure(home)
        _ensure(away)

        records[home]["played"] += 1
        records[away]["played"] += 1
        records[home]["gf"] += hs
        records[home]["ga"] += as_
        records[away]["gf"] += as_
        records[away]["ga"] += hs

        if hs > as_:
            records[home]["won"] += 1
            records[home]["points"] += 3
            records[away]["lost"] += 1
        elif hs == as_:
            records[home]["drawn"] += 1
            records[home]["points"] += 1
            records[away]["drawn"] += 1
            records[away]["points"] += 1
        else:
            records[away]["won"] += 1
            records[away]["points"] += 3
            records[home]["lost"] += 1

    df = pd.DataFrame(list(records.values()))
    df["gd"] = df["gf"] - df["ga"]
    return df.sort_values(["points", "gd", "gf"], ascending=False).reset_index(drop=True)


def get_position(table: pd.DataFrame, team: str) -> int:
    """Return 1-indexed league position for a team, or -1 if not found."""
    matches = table[table["team"] == team]
    if matches.empty:
        return -1
    return int(matches.index[0]) + 1
