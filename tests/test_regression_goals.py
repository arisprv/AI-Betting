import pandas as pd
import numpy as np
import pytest
from regression_goals import build_goals_features


def test_build_goals_features_returns_df():
    df = pd.DataFrame({
        "avg_goals_5": [1.5, 1.2],
        "avg_goals_against_5": [1.0, 1.3],
        "win_rate_5": [0.6, 0.4],
        "form_score_5": [0.5, -0.2],
        "goal_diff_avg_5": [0.5, -0.1],
        "clean_sheet_rate_5": [0.4, 0.2],
    })
    result = build_goals_features(df)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2


def test_build_goals_features_handles_missing():
    df = pd.DataFrame({"avg_goals_5": [1.5], "win_rate_5": [0.6]})
    result = build_goals_features(df)
    assert "avg_goals_5" in result.columns
    assert "win_rate_5" in result.columns
