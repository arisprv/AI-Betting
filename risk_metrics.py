"""Betting risk and performance metrics: Sharpe ratio, max drawdown, expectancy."""
import math
from typing import Optional
from logger import get_logger

log = get_logger(__name__)


def sharpe_ratio(returns: list[float], risk_free_rate: float = 0.0) -> Optional[float]:
    """Return annualised Sharpe ratio given a list of per-bet returns."""
    if len(returns) < 2:
        return None
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    std = math.sqrt(variance)
    if std == 0:
        return None
    return (mean - risk_free_rate) / std


def max_drawdown(balances: list[float]) -> float:
    """Return maximum peak-to-trough drawdown as a fraction of peak."""
    if not balances:
        return 0.0
    peak = balances[0]
    max_dd = 0.0
    for b in balances:
        if b > peak:
            peak = b
        dd = (peak - b) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, dd)
    return max_dd


def expectancy(wins: int, losses: int, avg_win: float, avg_loss: float) -> float:
    """Return per-bet expectancy (average profit per unit staked)."""
    total = wins + losses
    if total == 0:
        return 0.0
    win_rate = wins / total
    return win_rate * avg_win - (1 - win_rate) * avg_loss


def profit_factor(gross_profit: float, gross_loss: float) -> Optional[float]:
    """Return profit factor (gross wins / gross losses)."""
    if gross_loss == 0:
        return None
    return gross_profit / gross_loss


def recovery_factor(net_profit: float, max_dd_amount: float) -> Optional[float]:
    """Return recovery factor (net profit / max drawdown in currency)."""
    if max_dd_amount == 0:
        return None
    return net_profit / max_dd_amount
