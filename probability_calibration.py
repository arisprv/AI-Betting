"""Probability calibration analysis and reliability diagram data generation."""
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from logger import get_logger

log = get_logger(__name__)


def reliability_diagram_data(y_true: np.ndarray, y_prob: np.ndarray,
                               n_bins: int = 10) -> pd.DataFrame:
    """Return fraction_of_positives and mean_predicted_value for reliability diagram."""
    fraction_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="uniform")
    return pd.DataFrame({"mean_predicted": mean_pred, "fraction_positive": fraction_pos})


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Return Brier score — lower is better (0 = perfect)."""
    return float(np.mean((y_prob - y_true.astype(float)) ** 2))


def expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray,
                                 n_bins: int = 10) -> float:
    """Return ECE — weighted average of |confidence - accuracy| over bins."""
    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (y_prob >= lo) & (y_prob < hi)
        if mask.sum() == 0:
            continue
        acc = y_true[mask].mean()
        conf = y_prob[mask].mean()
        ece += mask.mean() * abs(conf - acc)
    return float(ece)


def calibration_report(y_true: np.ndarray, y_prob: np.ndarray) -> dict:
    """Return a summary of calibration metrics."""
    bs = brier_score(y_true, y_prob)
    ece = expected_calibration_error(y_true, y_prob)
    log.info("Brier Score: %.4f | ECE: %.4f", bs, ece)
    return {"brier_score": round(bs, 4), "ece": round(ece, 4)}
