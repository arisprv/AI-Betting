import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from logger import get_logger

log = get_logger(__name__)

DRIFT_THRESHOLD = 0.05


def compute_rolling_accuracy(predictions: pd.DataFrame, window: int = 20) -> pd.Series:
    if "correct" not in predictions:
        predictions = predictions.copy()
        predictions["correct"] = predictions["prediction"] == predictions["actual"]
    return predictions["correct"].rolling(window=window, min_periods=1).mean()


def detect_drift(baseline_acc: float, recent_acc: float, threshold: float = DRIFT_THRESHOLD) -> bool:
    drop = baseline_acc - recent_acc
    if drop > threshold:
        log.warning("Model drift detected: baseline %.3f -> recent %.3f (drop %.3f)", baseline_acc, recent_acc, drop)
        return True
    return False


def calibration_error(model_probs: np.ndarray, actual: np.ndarray, n_bins: int = 10) -> float:
    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (model_probs >= lo) & (model_probs < hi)
        if mask.sum() == 0:
            continue
        avg_prob = model_probs[mask].mean()
        avg_outcome = actual[mask].mean()
        ece += mask.mean() * abs(avg_prob - avg_outcome)
    return float(ece)


def monitor_model(predictions: pd.DataFrame, baseline_accuracy: float, window: int = 30) -> dict:
    recent = predictions.tail(window)
    if recent.empty:
        return {}
    recent_acc = accuracy_score(recent["actual"], recent["prediction"])
    drift = detect_drift(baseline_accuracy, recent_acc)
    rolling = compute_rolling_accuracy(predictions)
    return {
        "recent_accuracy": recent_acc,
        "drift_detected": drift,
        "rolling_accuracy": rolling.tolist(),
    }
