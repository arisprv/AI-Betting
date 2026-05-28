import numpy as np
import pandas as pd
import pytest
from model_monitor import compute_rolling_accuracy, detect_drift, calibration_error


@pytest.fixture
def predictions_df():
    return pd.DataFrame({
        "prediction": ["Home Win", "Draw", "Away Win", "Home Win", "Home Win"],
        "actual": ["Home Win", "Draw", "Home Win", "Home Win", "Away Win"],
    }).assign(correct=lambda df: df["prediction"] == df["actual"])


def test_rolling_accuracy_length(predictions_df):
    rolling = compute_rolling_accuracy(predictions_df, window=3)
    assert len(rolling) == len(predictions_df)


def test_rolling_accuracy_values(predictions_df):
    rolling = compute_rolling_accuracy(predictions_df, window=5)
    assert rolling.iloc[-1] == pytest.approx(0.6)


def test_detect_drift_triggered():
    assert detect_drift(0.65, 0.55, threshold=0.05) is True


def test_detect_drift_not_triggered():
    assert detect_drift(0.65, 0.63, threshold=0.05) is False


def test_calibration_error_perfect():
    probs = np.array([0.9, 0.1, 0.8, 0.2])
    actuals = np.array([1.0, 0.0, 1.0, 0.0])
    ece = calibration_error(probs, actuals)
    assert ece >= 0


def test_calibration_error_range():
    probs = np.random.uniform(0, 1, 100)
    actuals = (probs > 0.5).astype(float)
    ece = calibration_error(probs, actuals)
    assert 0.0 <= ece <= 1.0
