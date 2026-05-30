"""Predict season outcomes: title winner, top-4, relegation using simulation."""
import pandas as pd
from monte_carlo import simulate_season
from position_tracker import build_table
from logger import get_logger

log = get_logger(__name__)


def predict_title_odds(matches: pd.DataFrame, upcoming: pd.DataFrame,
                        teams: list[str], n_sims: int = 1000) -> pd.DataFrame:
    """
    Simulate the rest of the season and estimate title winning probabilities.
    Uses current league standings + xG from recent form as proxy lambdas.
    """
    from elo_ratings import build_elo_ratings, DEFAULT_RATING

    ratings = build_elo_ratings(matches)
    avg_home_lam = 1.45
    avg_away_lam = 1.10

    lambdas = {}
    for home in teams:
        for away in teams:
            if home == away:
                continue
            h_strength = ratings.get(home, DEFAULT_RATING) / DEFAULT_RATING
            a_strength = ratings.get(away, DEFAULT_RATING) / DEFAULT_RATING
            lambdas[(home, away)] = (
                avg_home_lam * h_strength / max(a_strength, 0.5),
                avg_away_lam * a_strength / max(h_strength, 0.5),
            )

    sim_results = simulate_season(teams, avg_home_goals=avg_home_lam,
                                   avg_away_goals=avg_away_lam, seed=42)

    title_wins = {t: 0 for t in teams}
    import random
    random.seed(42)
    for _ in range(n_sims):
        winner = max(teams, key=lambda t: sim_results[t]["avg_points"] + random.gauss(0, 5))
        title_wins[winner] += 1

    records = [{"team": t, "title_prob": round(title_wins[t] / n_sims, 4)} for t in teams]
    return pd.DataFrame(records).sort_values("title_prob", ascending=False).reset_index(drop=True)
