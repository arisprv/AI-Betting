"""Closing Line Value (CLV) — the gold standard of sharp betting evaluation."""
from logger import get_logger

log = get_logger(__name__)


def clv(opening_odds: float, closing_odds: float) -> float:
    """
    Return CLV as a percentage.
    Positive = beat the closing line (good).
    Negative = closing line moved against you (bad).
    """
    if closing_odds <= 0 or opening_odds <= 0:
        return 0.0
    implied_open = 1 / opening_odds
    implied_close = 1 / closing_odds
    return (implied_open - implied_close) / implied_close * 100


def average_clv(clv_values: list[float]) -> float:
    """Return average CLV across a series of bets."""
    if not clv_values:
        return 0.0
    return sum(clv_values) / len(clv_values)


def clv_from_bets(bets: list[dict]) -> list[float]:
    """
    Compute CLV for each bet dict that has 'opening_odds' and 'closing_odds' keys.
    """
    return [
        clv(b.get("opening_odds", 0), b.get("closing_odds", 0))
        for b in bets
        if b.get("opening_odds") and b.get("closing_odds")
    ]


def interpret_clv(avg_clv: float) -> str:
    """Return a qualitative assessment of average CLV."""
    if avg_clv > 3:
        return "Excellent — consistently beating the market"
    elif avg_clv > 1:
        return "Good — ahead of the closing line"
    elif avg_clv > 0:
        return "Slightly positive — marginal edge"
    elif avg_clv > -1:
        return "Slightly negative — near break-even"
    else:
        return "Poor — losing to the closing line"
