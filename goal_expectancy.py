"""Compute expected goals (xG) for upcoming matches using Dixon-Coles attack/defence strengths."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def attack_strength(team_avg_scored: float, league_avg_scored: float) -> float:
    """Attack strength relative to league average."""
    return team_avg_scored / league_avg_scored if league_avg_scored > 0 else 1.0


def defence_strength(team_avg_conceded: float, league_avg_conceded: float) -> float:
    """Defence strength relative to league average (higher = weaker defence)."""
    return team_avg_conceded / league_avg_conceded if league_avg_conceded > 0 else 1.0


def expected_goals(home_attack: float, away_defence: float, league_avg_home: float) -> float:
    """Expected goals for home team."""
    return round(home_attack * away_defence * league_avg_home, 3)


def match_xg(
    home_avg_scored: float,
    home_avg_conceded: float,
    away_avg_scored: float,
    away_avg_conceded: float,
    league_avg_home: float = 1.5,
    league_avg_away: float = 1.1,
) -> dict[str, float]:
    """Return home and away xG for a match."""
    h_att = attack_strength(home_avg_scored, league_avg_home)
    h_def = defence_strength(home_avg_conceded, league_avg_away)
    a_att = attack_strength(away_avg_scored, league_avg_away)
    a_def = defence_strength(away_avg_conceded, league_avg_home)

    home_xg = expected_goals(h_att, a_def, league_avg_home)
    away_xg = expected_goals(a_att, h_def, league_avg_away)

    return {"home_xg": home_xg, "away_xg": away_xg, "total_xg": round(home_xg + away_xg, 3)}


def enrich_upcoming_with_xg(upcoming: pd.DataFrame, features: pd.DataFrame,
                              league_avg_home: float = 1.5,
                              league_avg_away: float = 1.1) -> pd.DataFrame:
    """Add xG columns to each upcoming match."""
    rows = []
    for _, match in upcoming.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        home_f = features[(features["team"] == home) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        away_f = features[(features["team"] == away) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        if home_f.empty or away_f.empty:
            rows.append({})
            continue
        xg = match_xg(
            home_f["avg_goals_5"].values[0], home_f["avg_goals_against_5"].values[0],
            away_f["avg_goals_5"].values[0], away_f["avg_goals_against_5"].values[0],
            league_avg_home, league_avg_away,
        )
        rows.append(xg)
    xg_df = pd.DataFrame(rows)
    return pd.concat([upcoming.reset_index(drop=True), xg_df], axis=1)
