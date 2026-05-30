import numpy as np
import pytest
from probability_calibration import brier_score, expected_calibration_error, calibration_report


def test_brier_score_perfect():
    y_true = np.array([1, 0, 1, 0])
    y_prob = np.array([1.0, 0.0, 1.0, 0.0])
    assert brier_score(y_true, y_prob) == pytest.approx(0.0)


def test_brier_score_worst():
    y_true = np.array([1, 0, 1, 0])
    y_prob = np.array([0.0, 1.0, 0.0, 1.0])
    assert brier_score(y_true, y_prob) == pytest.approx(1.0)


def test_brier_score_range():
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 100)
    y_prob = np.random.uniform(0, 1, 100)
    assert 0.0 <= brier_score(y_true, y_prob) <= 1.0


def test_ece_perfect_calibration():
    y_true = np.array([1, 0] * 50)
    y_prob = np.array([1.0, 0.0] * 50)
    ece = expected_calibration_error(y_true, y_prob)
    assert ece < 0.1


def test_calibration_report_keys():
    y_true = np.array([1, 0, 1, 0, 1])
    y_prob = np.array([0.7, 0.3, 0.6, 0.4, 0.8])
    report = calibration_report(y_true, y_prob)
    assert "brier_score" in report and "ece" in report
