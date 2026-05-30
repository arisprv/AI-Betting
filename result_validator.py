"""Validate model predictions against settled match results."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)

RESULT_MAP = {1: "Home Win", 0: "Draw", -1: "Away Win"}


def classify_result(home_score: int, away_score: int) -> str:
    if home_score > away_score:
        return "Home Win"
    elif home_score < away_score:
        return "Away Win"
    return "Draw"


def validate_predictions(predictions: pd.DataFrame, results: pd.DataFrame,
                          match_col: str = "match") -> pd.DataFrame:
    """
    Join predictions with actual results and add correctness flag.
    predictions: has columns [match, prediction, confidence]
    results: has columns [match, homeScore, awayScore]
    """
    results = results.copy()
    results["actual"] = results.apply(
        lambda r: classify_result(r["homeScore"], r["awayScore"]), axis=1
    )
    merged = predictions.merge(results[[match_col, "actual"]], on=match_col, how="left")
    merged["correct"] = merged["prediction"] == merged["actual"]
    return merged


def accuracy_by_confidence(validated: pd.DataFrame, bins: int = 5) -> pd.DataFrame:
    """Return accuracy broken down by confidence bin."""
    import numpy as np
    thresholds = np.linspace(0.5, 1.0, bins + 1)
    rows = []
    for lo, hi in zip(thresholds[:-1], thresholds[1:]):
        bucket = validated[(validated["confidence"] >= lo) & (validated["confidence"] < hi)]
        rows.append({
            "conf_bin": f"{lo:.2f}-{hi:.2f}",
            "count": len(bucket),
            "accuracy": bucket["correct"].mean() if not bucket.empty else None,
        })
    return pd.DataFrame(rows)
