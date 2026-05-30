"""Draw No Bet (DNB) market probability and value calculation."""
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def dnb_probabilities(home_lambda: float, away_lambda: float) -> dict[str, float]:
    """
    Return Draw No Bet probabilities: Home or Away only (draw is void).
    The probabilities are normalised excluding draws.
    """
    probs = score_probabilities(home_lambda, away_lambda)
    home_win = sum(p for (hg, ag), p in probs.items() if hg > ag)
    draw = sum(p for (hg, ag), p in probs.items() if hg == ag)
    away_win = sum(p for (hg, ag), p in probs.items() if hg < ag)

    non_draw = home_win + away_win
    if non_draw == 0:
        return {"dnb_home": 0.5, "dnb_away": 0.5, "draw_prob": draw}

    return {
        "dnb_home": round(home_win / non_draw, 4),
        "dnb_away": round(away_win / non_draw, 4),
        "draw_prob": round(draw, 4),
    }


def dnb_fair_odds(home_lambda: float, away_lambda: float) -> dict[str, float]:
    """Return fair DNB odds (no margin)."""
    probs = dnb_probabilities(home_lambda, away_lambda)
    return {
        "dnb_home_odds": round(1 / probs["dnb_home"], 3) if probs["dnb_home"] > 0 else 0,
        "dnb_away_odds": round(1 / probs["dnb_away"], 3) if probs["dnb_away"] > 0 else 0,
    }


def dnb_ev(model_prob: float, market_odds: float, draw_prob: float) -> float:
    """
    Expected value on a DNB bet.
    If draw: stake refunded (EV contribution = 0).
    """
    return model_prob * (market_odds - 1) - (1 - model_prob - draw_prob) * 1
