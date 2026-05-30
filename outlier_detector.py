"""Detect outlier matches that may skew model training."""
import pandas as pd
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def z_score_outliers(df: pd.DataFrame, col: str, threshold: float = 3.0) -> pd.DataFrame:
    """Return rows where |z-score| of col exceeds threshold."""
    mean = df[col].mean()
    std = df[col].std()
    if std == 0:
        return pd.DataFrame()
    z = (df[col] - mean) / std
    return df[z.abs() > threshold]


def total_goals_outliers(matches: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """Flag matches with unusually high total goals."""
    df = matches.copy()
    df["total_goals"] = df["homeScore"] + df["awayScore"]
    outliers = z_score_outliers(df, "total_goals", threshold)
    if not outliers.empty:
        log.warning("Found %d high-scoring outlier matches", len(outliers))
    return outliers


def goal_diff_outliers(matches: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """Flag matches with unusually large goal differences (e.g. 7-0)."""
    df = matches.copy()
    df["goal_diff"] = (df["homeScore"] - df["awayScore"]).abs()
    return z_score_outliers(df, "goal_diff", threshold)


def remove_outlier_matches(matches: pd.DataFrame, total_goals_z: float = 3.5,
                            goal_diff_z: float = 3.5) -> pd.DataFrame:
    """Remove statistical outlier matches from the training set."""
    tg_out = set(total_goals_outliers(matches, total_goals_z).index)
    gd_out = set(goal_diff_outliers(matches, goal_diff_z).index)
    outlier_idx = tg_out | gd_out
    cleaned = matches.drop(index=outlier_idx)
    if outlier_idx:
        log.info("Removed %d outlier matches from dataset", len(outlier_idx))
    return cleaned.reset_index(drop=True)
