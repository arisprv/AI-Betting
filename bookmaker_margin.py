"""Calculate bookmaker margin (overround) and true probabilities."""
from logger import get_logger

log = get_logger(__name__)


def overround(home_odds: float, draw_odds: float, away_odds: float) -> float:
    """Return the bookmaker's overround (total implied probability > 1.0)."""
    if any(o is None or o <= 0 for o in [home_odds, draw_odds, away_odds]):
        return 0.0
    return (1 / home_odds) + (1 / draw_odds) + (1 / away_odds) - 1.0


def true_probabilities(home_odds: float, draw_odds: float, away_odds: float) -> dict[str, float]:
    """Remove the bookmaker margin to get fair probabilities."""
    implied = {
        "Home Win": 1 / home_odds if home_odds else 0,
        "Draw": 1 / draw_odds if draw_odds else 0,
        "Away Win": 1 / away_odds if away_odds else 0,
    }
    total = sum(implied.values())
    if total == 0:
        return implied
    return {k: v / total for k, v in implied.items()}


def margin_percent(home_odds: float, draw_odds: float, away_odds: float) -> float:
    """Return margin as a percentage."""
    return overround(home_odds, draw_odds, away_odds) * 100


def fair_odds(home_odds: float, draw_odds: float, away_odds: float) -> dict[str, float]:
    """Return the fair decimal odds (no margin)."""
    probs = true_probabilities(home_odds, draw_odds, away_odds)
    return {k: round(1 / v, 3) if v > 0 else float("inf") for k, v in probs.items()}
