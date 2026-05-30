import pandas as pd
import pytest
from feature_selector import variance_filter, correlation_filter


def test_variance_filter_removes_constant():
    df = pd.DataFrame({
        "always_zero": [0.0] * 10,
        "normal": [1.0, 2.0, 3.0, 1.5, 2.5, 1.0, 2.0, 3.0, 1.5, 2.5],
    })
    selected = variance_filter(df, threshold=0.001)
    assert "always_zero" not in selected
    assert "normal" in selected


def test_variance_filter_keeps_variable_features():
    df = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 1.0, 2.0],
        "b": [3.0, 1.0, 2.0, 3.0, 1.0],
    })
    selected = variance_filter(df)
    assert set(selected) == {"a", "b"}


def test_correlation_filter_removes_duplicate():
    df = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 4.0, 5.0],
        "b": [2.0, 4.0, 6.0, 8.0, 10.0],  # perfectly correlated with a
        "c": [1.0, 0.5, 2.0, 1.5, 0.8],
    })
    selected = correlation_filter(df, threshold=0.9)
    assert len(selected) < 3
