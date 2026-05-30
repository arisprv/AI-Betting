import pandas as pd
import pytest
from outlier_detector import z_score_outliers


def test_z_score_no_outliers():
    df = pd.DataFrame({"goals": [1, 2, 1, 2, 1, 2, 1]})
    result = z_score_outliers(df, "goals", threshold=3.0)
    assert len(result) == 0


def test_z_score_finds_outlier():
    df = pd.DataFrame({"goals": [1, 1, 1, 1, 1, 1, 100]})
    result = z_score_outliers(df, "goals", threshold=2.0)
    assert len(result) == 1
    assert result["goals"].iloc[0] == 100


def test_z_score_zero_variance():
    df = pd.DataFrame({"goals": [2, 2, 2, 2]})
    result = z_score_outliers(df, "goals", threshold=2.0)
    assert len(result) == 0
