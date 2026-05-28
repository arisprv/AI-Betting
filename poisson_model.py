"""Dixon-Coles inspired Poisson model for predicting exact scores and probabilities."""
import math
from functools import lru_cache
from logger import get_logger

log = get_logger(__name__)

MAX_GOALS = 8


@lru_cache(maxsize=512)
def _poisson_pmf(lam: float, k: int) -> float:
    return (lam ** k * math.exp(-lam)) / math.factorial(k)


def score_probabilities(home_lambda: float, away_lambda: float) -> dict[tuple[int, int], float]:
    """Return a dict mapping (home_goals, away_goals) -> probability."""
    probs = {}
    for hg in range(MAX_GOALS + 1):
        for ag in range(MAX_GOALS + 1):
            probs[(hg, ag)] = _poisson_pmf(home_lambda, hg) * _poisson_pmf(away_lambda, ag)
    return probs


def outcome_probs(home_lambda: float, away_lambda: float) -> dict[str, float]:
    """Aggregate score probabilities into Home Win / Draw / Away Win."""
    score_probs = score_probabilities(home_lambda, away_lambda)
    result = {"Home Win": 0.0, "Draw": 0.0, "Away Win": 0.0}
    for (hg, ag), p in score_probs.items():
        if hg > ag:
            result["Home Win"] += p
        elif hg == ag:
            result["Draw"] += p
        else:
            result["Away Win"] += p
    return result


def estimate_lambda(avg_goals_scored: float, avg_goals_conceded: float,
                    league_avg_home: float = 1.5, league_avg_away: float = 1.2) -> float:
    """Estimate expected goals using attack/defence strengths."""
    if league_avg_home == 0 or league_avg_away == 0:
        return avg_goals_scored
    attack = avg_goals_scored / league_avg_home
    defence = avg_goals_conceded / league_avg_away
    return attack * defence * league_avg_home
