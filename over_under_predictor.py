"""Predict over/under goals markets using team attacking/defensive stats."""
import pandas as pd
import numpy as np
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def over_prob(home_lambda: float, away_lambda: float, threshold: float = 2.5) -> float:
    """Probability that total goals exceed threshold via Poisson model."""
    probs = score_probabilities(home_lambda, away_lambda)
    return sum(p for (hg, ag), p in probs.items() if hg + ag > threshold)


def under_prob(home_lambda: float, away_lambda: float, threshold: float = 2.5) -> float:
    return 1 - over_prob(home_lambda, away_lambda, threshold)


def predict_over_under(
    home_avg_goals: float,
    away_avg_goals: float,
    home_avg_conceded: float,
    away_avg_conceded: float,
    threshold: float = 2.5,
) -> dict[str, float]:
    home_lambda = (home_avg_goals + away_avg_conceded) / 2
    away_lambda = (away_avg_goals + home_avg_conceded) / 2
    p_over = over_prob(home_lambda, away_lambda, threshold)
    return {
        f"over_{threshold}": round(p_over, 4),
        f"under_{threshold}": round(1 - p_over, 4),
        "home_xg": round(home_lambda, 3),
        "away_xg": round(away_lambda, 3),
    }


def batch_over_under(upcoming: pd.DataFrame, features: pd.DataFrame, threshold: float = 2.5) -> pd.DataFrame:
    results = []
    for _, match in upcoming.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        home_s = features[(features["team"] == home) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        away_s = features[(features["team"] == away) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        if home_s.empty or away_s.empty:
            continue
        pred = predict_over_under(
            home_s["avg_goals_5"].values[0],
            away_s["avg_goals_5"].values[0],
            home_s["avg_goals_against_5"].values[0],
            away_s["avg_goals_against_5"].values[0],
            threshold,
        )
        pred["match"] = f"{home} vs {away}"
        pred["date"] = date
        results.append(pred)
    return pd.DataFrame(results)
