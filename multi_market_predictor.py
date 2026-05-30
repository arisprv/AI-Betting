"""Combine 1X2, over/under, BTTS, and correct score into one prediction card."""
import pandas as pd
from poisson_model import score_probabilities
from goal_expectancy import match_xg
from over_under_predictor import over_prob, under_prob
from btts_predictor import btts_prob
from correct_score_predictor import top_n_scores
from draw_no_bet import dnb_probabilities
from logger import get_logger

log = get_logger(__name__)


def full_prediction_card(
    home: str,
    away: str,
    home_avg_scored: float,
    home_avg_conceded: float,
    away_avg_scored: float,
    away_avg_conceded: float,
    league_avg_home: float = 1.5,
    league_avg_away: float = 1.1,
) -> dict:
    """Return a comprehensive prediction card for a single match."""
    xg = match_xg(home_avg_scored, home_avg_conceded, away_avg_scored,
                   away_avg_conceded, league_avg_home, league_avg_away)
    h_lam, a_lam = xg["home_xg"], xg["away_xg"]

    probs = score_probabilities(h_lam, a_lam)
    home_win = sum(p for (hg, ag), p in probs.items() if hg > ag)
    draw_p = sum(p for (hg, ag), p in probs.items() if hg == ag)
    away_win = sum(p for (hg, ag), p in probs.items() if hg < ag)

    dnb = dnb_probabilities(h_lam, a_lam)
    top_scores = top_n_scores(h_lam, a_lam, n=5)

    return {
        "match": f"{home} vs {away}",
        "home_xg": h_lam,
        "away_xg": a_lam,
        "1x2": {
            "Home Win": round(home_win, 4),
            "Draw": round(draw_p, 4),
            "Away Win": round(away_win, 4),
        },
        "over_2_5": round(over_prob(h_lam, a_lam, 2.5), 4),
        "under_2_5": round(under_prob(h_lam, a_lam, 2.5), 4),
        "btts_yes": round(btts_prob(h_lam, a_lam), 4),
        "dnb_home": dnb["dnb_home"],
        "dnb_away": dnb["dnb_away"],
        "top_scores": [{"score": f"{hg}-{ag}", "prob": round(p, 4)} for (hg, ag), p in top_scores],
    }
