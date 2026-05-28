import pandas as pd
from typing import Optional
from logger import get_logger

log = get_logger(__name__)


def compute_roi(bets: pd.DataFrame) -> Optional[float]:
    if bets.empty or "stake" not in bets or "pnl" not in bets:
        return None
    total_staked = bets["stake"].sum()
    return bets["pnl"].sum() / total_staked if total_staked > 0 else None


def compute_win_rate(bets: pd.DataFrame) -> Optional[float]:
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


def print_summary(bets: pd.DataFrame) -> None:
    roi = compute_roi(bets)
    wr = compute_win_rate(bets)
    total_pnl = bets["pnl"].sum() if not bets.empty else 0
    log.info("=== Performance Summary ===")
    log.info("Total bets:  %d", len(bets))
    log.info("Total P&L:   %.2f", total_pnl)
    log.info("ROI:         %.1f%%", (roi or 0) * 100)
    log.info("Win rate:    %.1f%%", (wr or 0) * 100)
