import pandas as pd
from typing import Optional
from team_name_normalizer import find_best_match
from logger import get_logger

log = get_logger(__name__)


def normalize_overround(odds_dict: dict[str, float]) -> dict[str, float]:
    total_implied = sum(1 / v for v in odds_dict.values() if v and v > 0)
    if total_implied == 0:
        return odds_dict
    return {k: (1 / v) / total_implied for k, v in odds_dict.items() if v and v > 0}


def expected_value(model_prob: float, decimal_odds: float) -> float:
    return model_prob * decimal_odds - 1


def is_value_bet(model_prob: float, decimal_odds: float, min_edge: float = 0.02) -> bool:
    return expected_value(model_prob, decimal_odds) > min_edge


def best_odds(odds_df: pd.DataFrame, home: str, away: str, market: str) -> Optional[float]:
    matches = odds_df[
        (odds_df["home_team"] == home) & (odds_df["away_team"] == away)
    ]
    if matches.empty:
        home_norm = find_best_match(home, odds_df["home_team"].tolist())
        away_norm = find_best_match(away, odds_df["away_team"].tolist())
        if home_norm and away_norm:
            matches = odds_df[(odds_df["home_team"] == home_norm) & (odds_df["away_team"] == away_norm)]
    if matches.empty:
        return None
    col_map = {"Home Win": "home_odds", "Draw": "draw_odds", "Away Win": "away_odds"}
    col = col_map.get(market)
    if not col or col not in matches:
        return None
    valid = matches[col].dropna()
    return float(valid.max()) if not valid.empty else None


def summarize_market(odds_df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for (home, away), group in odds_df.groupby(["home_team", "away_team"]):
        records.append({
            "home_team": home,
            "away_team": away,
            "best_home_odds": group["home_odds"].max(),
            "best_draw_odds": group["draw_odds"].max(),
            "best_away_odds": group["away_odds"].max(),
            "bookmakers_count": group["bookmaker"].nunique(),
        })
    return pd.DataFrame(records)
