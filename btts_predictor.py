"""Predict Both Teams To Score market."""
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def btts_prob(home_lambda: float, away_lambda: float) -> float:
    """Probability both teams score at least one goal."""
    probs = score_probabilities(home_lambda, away_lambda)
    return sum(p for (hg, ag), p in probs.items() if hg > 0 and ag > 0)


def no_btts_prob(home_lambda: float, away_lambda: float) -> float:
    return 1 - btts_prob(home_lambda, away_lambda)


def predict_btts(
    home_avg_goals: float,
    away_avg_goals: float,
    home_avg_conceded: float,
    away_avg_conceded: float,
) -> dict[str, float]:
    """Return BTTS Yes/No probabilities using xG estimates."""
    home_lambda = (home_avg_goals + away_avg_conceded) / 2
    away_lambda = (away_avg_goals + home_avg_conceded) / 2
    p_yes = btts_prob(home_lambda, away_lambda)
    return {
        "btts_yes": round(p_yes, 4),
        "btts_no": round(1 - p_yes, 4),
        "home_xg": round(home_lambda, 3),
        "away_xg": round(away_lambda, 3),
    }
