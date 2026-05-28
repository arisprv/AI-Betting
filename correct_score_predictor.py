"""Predict correct score probabilities for a football match."""
from poisson_model import score_probabilities
from logger import get_logger

log = get_logger(__name__)


def top_n_scores(home_lambda: float, away_lambda: float, n: int = 10) -> list[tuple[tuple[int, int], float]]:
    """Return the top-n most likely scorelines with their probabilities."""
    probs = score_probabilities(home_lambda, away_lambda)
    sorted_probs = sorted(probs.items(), key=lambda x: -x[1])
    return sorted_probs[:n]


def correct_score_report(home: str, away: str, home_lambda: float, away_lambda: float,
                          n: int = 5) -> str:
    """Return a formatted string of the top-n predicted scores."""
    top = top_n_scores(home_lambda, away_lambda, n)
    lines = [f"Correct score predictions: {home} vs {away}", "-" * 40]
    for (hg, ag), prob in top:
        lines.append(f"  {hg}-{ag}   {prob * 100:.2f}%")
    return "\n".join(lines)


def most_likely_score(home_lambda: float, away_lambda: float) -> tuple[int, int]:
    """Return the single most probable scoreline."""
    probs = score_probabilities(home_lambda, away_lambda)
    return max(probs, key=probs.get)
