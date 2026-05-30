"""Season-level aggregate statistics per league and team."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def league_season_summary(matches: pd.DataFrame) -> pd.DataFrame:
    """Return season-level stats per league: total matches, goals, avg goals."""
    df = matches.copy()
    df["total_goals"] = df["homeScore"] + df["awayScore"]
    summary = df.groupby("league").agg(
        matches=("total_goals", "count"),
        total_goals=("total_goals", "sum"),
        avg_goals=("total_goals", "mean"),
        home_wins=("homeScore", lambda x: (x > df.loc[x.index, "awayScore"]).sum()),
    ).reset_index()
    summary["home_win_rate"] = summary["home_wins"] / summary["matches"]
    return summary


def team_season_stats(matches: pd.DataFrame, team: str) -> dict:
    """Aggregate season stats for a single team."""
    home = matches[matches["homeTeam"] == team]
    away = matches[matches["awayTeam"] == team]

    goals_scored = int(home["homeScore"].sum() + away["awayScore"].sum())
    goals_conceded = int(home["awayScore"].sum() + away["homeScore"].sum())
    played = len(home) + len(away)

    home_wins = int((home["homeScore"] > home["awayScore"]).sum())
    away_wins = int((away["awayScore"] > away["homeScore"]).sum())
    draws = played - home_wins - away_wins - int(
        (home["homeScore"] < home["awayScore"]).sum() +
        (away["awayScore"] < away["homeScore"]).sum()
    )
    points = home_wins * 3 + away_wins * 3 + draws

    return {
        "team": team,
        "played": played,
        "goals_scored": goals_scored,
        "goals_conceded": goals_conceded,
        "goal_diff": goals_scored - goals_conceded,
        "points": points,
        "avg_goals_scored": round(goals_scored / played, 2) if played else 0,
        "avg_goals_conceded": round(goals_conceded / played, 2) if played else 0,
    }
