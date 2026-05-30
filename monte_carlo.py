"""Monte Carlo simulation for match outcome probability estimation."""
import random
from collections import Counter
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def simulate_match(home_lambda: float, away_lambda: float, n_sims: int = 10_000) -> dict[str, float]:
    """Simulate a match n_sims times and return outcome frequencies."""
    counts: Counter = Counter()
    for _ in range(n_sims):
        hg = _sample_poisson(home_lambda)
        ag = _sample_poisson(away_lambda)
        if hg > ag:
            counts["Home Win"] += 1
        elif hg == ag:
            counts["Draw"] += 1
        else:
            counts["Away Win"] += 1
    return {k: v / n_sims for k, v in counts.items()}


def _sample_poisson(lam: float) -> int:
    """Sample from Poisson distribution using Knuth algorithm."""
    import math
    L = math.exp(-lam)
    k, p = 0, 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1


def simulate_season(teams: list[str], lambdas: dict[tuple[str, str], tuple[float, float]],
                    n_sims: int = 1_000) -> dict[str, dict]:
    """Simulate a full round-robin season and return points distributions."""
    points_dist: dict[str, list[int]] = {t: [] for t in teams}

    for _ in range(n_sims):
        points: dict[str, int] = {t: 0 for t in teams}
        for home in teams:
            for away in teams:
                if home == away:
                    continue
                h_lam, a_lam = lambdas.get((home, away), (1.35, 1.10))
                hg = _sample_poisson(h_lam)
                ag = _sample_poisson(a_lam)
                if hg > ag:
                    points[home] += 3
                elif hg == ag:
                    points[home] += 1
                    points[away] += 1
                else:
                    points[away] += 3
        for t in teams:
            points_dist[t].append(points[t])

    results = {}
    for t in teams:
        pts = points_dist[t]
        results[t] = {
            "avg_points": sum(pts) / len(pts),
            "min_points": min(pts),
            "max_points": max(pts),
        }
    return results
