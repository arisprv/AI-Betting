"""Comprehensive value bet identification combining model probs, CLV, and EV."""
from closing_line_value import clv
from bookmaker_margin import true_probabilities
from logger import get_logger

log = get_logger(__name__)


def composite_value_score(
    model_prob: float,
    market_home_odds: float,
    market_draw_odds: float,
    market_away_odds: float,
    outcome: str,
    opening_odds: float = None,
    closing_odds: float = None,
) -> dict:
    """
    Return a composite value assessment combining:
    - Model edge vs market
    - Expected value
    - CLV (if opening odds provided)
    """
    true_probs = true_probabilities(market_home_odds, market_draw_odds, market_away_odds)
    market_prob = true_probs.get(outcome, 0)
    edge = model_prob - market_prob

    market_odds = {"Home Win": market_home_odds, "Draw": market_draw_odds, "Away Win": market_away_odds}
    best_odds = market_odds.get(outcome, 0)
    ev = model_prob * best_odds - 1 if best_odds > 0 else 0.0

    clv_val = clv(opening_odds, closing_odds) if opening_odds and closing_odds else None

    score = edge * 0.5 + ev * 0.3 + (clv_val / 100 if clv_val else 0) * 0.2

    return {
        "outcome": outcome,
        "model_prob": round(model_prob, 4),
        "market_prob": round(market_prob, 4),
        "edge": round(edge, 4),
        "ev": round(ev, 4),
        "clv": round(clv_val, 2) if clv_val is not None else None,
        "composite_score": round(score, 4),
        "is_value": edge > 0.02 and ev > 0,
    }
