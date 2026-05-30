"""Analyse bookmaker market efficiency and exploit edges."""
import pandas as pd
from bookmaker_margin import overround, true_probabilities
from logger import get_logger

log = get_logger(__name__)


def market_efficiency_score(odds_df: pd.DataFrame) -> pd.Series:
    """Return per-match overround as a measure of market efficiency (lower = sharper)."""
    scores = []
    for _, row in odds_df.iterrows():
        margin = overround(
            row.get("home_odds", 0),
            row.get("draw_odds", 0),
            row.get("away_odds", 0),
        )
        scores.append(margin)
    return pd.Series(scores, index=odds_df.index, name="overround")


def find_soft_lines(odds_df: pd.DataFrame, threshold: float = 0.06) -> pd.DataFrame:
    """Return matches where the overround exceeds threshold — soft/inefficient markets."""
    scores = market_efficiency_score(odds_df)
    soft = odds_df[scores > threshold].copy()
    soft["overround"] = scores[soft.index]
    log.info("Found %d soft-line matches (overround > %.2f)", len(soft), threshold)
    return soft


def pinnicle_margin(home_odds: float, draw_odds: float, away_odds: float) -> float:
    """Estimate true margin by comparing to Pinnacle-style tight lines (proxy)."""
    return overround(home_odds, draw_odds, away_odds) * 100


def model_vs_market(model_prob: float, market_home_odds: float,
                     market_draw_odds: float, market_away_odds: float,
                     outcome: str) -> dict:
    """Compare model probability against market-implied probability."""
    true_probs = true_probabilities(market_home_odds, market_draw_odds, market_away_odds)
    market_prob = true_probs.get(outcome, 0)
    edge = model_prob - market_prob
    return {
        "model_prob": round(model_prob, 4),
        "market_prob": round(market_prob, 4),
        "edge": round(edge, 4),
        "is_value": edge > 0,
    }
