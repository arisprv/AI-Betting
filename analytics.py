"""Performance analytics for bet tracking — ROI, win rate, breakdowns."""
import pandas as pd
from typing import Optional
from logger import get_logger

log = get_logger(__name__)


def compute_roi(bets: pd.DataFrame) -> Optional[float]:
    """Return total P&L / total staked, or None if no bets were placed."""
    if bets.empty or "stake" not in bets or "pnl" not in bets:
        return None
    total_staked = bets["stake"].sum()
    return bets["pnl"].sum() / total_staked if total_staked > 0 else None


def compute_win_rate(bets: pd.DataFrame) -> Optional[float]:
    """Return fraction of bets won, or None if no bets were placed."""
    if bets.empty or "won" not in bets:
        return None
    return bets["won"].mean()


def by_league(bets: pd.DataFrame) -> pd.DataFrame:
    if bets.empty:
        return pd.DataFrame()
    return bets.groupby("league").agg(
        bets_count=("pnl", "count"),
        total_pnl=("pnl", "sum"),
        total_staked=("stake", "sum"),
        win_rate=("won", "mean"),
    ).assign(roi=lambda df: df["total_pnl"] / df["total_staked"])


def by_prediction(bets: pd.DataFrame) -> pd.DataFrame:
    if bets.empty:
        return pd.DataFrame()
    return bets.groupby("prediction").agg(
        bets_count=("pnl", "count"),
        total_pnl=("pnl", "sum"),
        total_staked=("stake", "sum"),
        win_rate=("won", "mean"),
    ).assign(roi=lambda df: df["total_pnl"] / df["total_staked"])


def cumulative_pnl(bets: pd.DataFrame) -> pd.Series:
    return bets["pnl"].cumsum()


def monthly_summary(bets: pd.DataFrame) -> pd.DataFrame:
    if bets.empty or "date" not in bets:
        return pd.DataFrame()
    bets = bets.copy()
    bets["month"] = pd.to_datetime(bets["date"]).dt.to_period("M")
    return bets.groupby("month").agg(
        bets_count=("pnl", "count"),
        total_pnl=("pnl", "sum"),
        total_staked=("stake", "sum"),
    ).assign(roi=lambda df: df["total_pnl"] / df["total_staked"])


def sharpe_ratio_bets(bets: pd.DataFrame) -> Optional[float]:
    """Return Sharpe ratio of per-bet returns (pnl / stake)."""
    if bets.empty or "pnl" not in bets or "stake" not in bets:
        return None
    returns = (bets["pnl"] / bets["stake"].replace(0, 1)).tolist()
    if len(returns) < 2:
        return None
    import math
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    std = math.sqrt(variance)
    return (mean / std) if std > 0 else None


def max_drawdown_bets(bets: pd.DataFrame) -> float:
    """Return maximum peak-to-trough drawdown of running balance."""
    if bets.empty or "balance" not in bets:
        return 0.0
    balances = bets["balance"].tolist()
    peak = balances[0]
    max_dd = 0.0
    for b in balances:
        peak = max(peak, b)
        dd = (peak - b) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, dd)
    return round(max_dd, 4)


def print_summary(bets: pd.DataFrame) -> None:
    roi = compute_roi(bets)
    wr = compute_win_rate(bets)
    total_pnl = bets["pnl"].sum() if not bets.empty else 0
    log.info("=== Performance Summary ===")
    log.info("Total bets:  %d", len(bets))
    log.info("Total P&L:   %.2f", total_pnl)
    log.info("ROI:         %.1f%%", (roi or 0) * 100)
    log.info("Win rate:    %.1f%%", (wr or 0) * 100)
    log.info("Max DD:      %.1f%%", max_drawdown_bets(bets) * 100)
    sr = sharpe_ratio_bets(bets)
    log.info("Sharpe:      %s", f"{sr:.3f}" if sr is not None else "N/A")
