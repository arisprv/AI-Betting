"""Asian Handicap calculation utilities."""
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def asian_handicap_prob(home_lambda: float, away_lambda: float, handicap: float) -> dict[str, float]:
    """
    Compute Asian Handicap probabilities.
    A positive handicap means the home team is the underdog (gets goals added).
    """
    probs = score_probabilities(home_lambda, away_lambda)
    home_win = draw = away_win = 0.0

    for (hg, ag), p in probs.items():
        adjusted_home = hg + handicap
        if adjusted_home > ag:
            home_win += p
        elif adjusted_home == ag:
            draw += p
        else:
            away_win += p

    return {
        "ah_home": round(home_win, 4),
        "ah_draw": round(draw, 4),
        "ah_away": round(away_win, 4),
        "handicap": handicap,
    }


def whole_handicap_probs(home_lambda: float, away_lambda: float,
                          handicaps: list[float] = None) -> list[dict]:
    """Return AH probabilities for a range of handicaps."""
    if handicaps is None:
        handicaps = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    return [asian_handicap_prob(home_lambda, away_lambda, h) for h in handicaps]
