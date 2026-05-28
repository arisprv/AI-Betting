import pandas as pd
import pytest
from xg_features import compute_xg_ratio, add_xg_features


def test_xg_ratio_above_average():
    result = compute_xg_ratio(2.0, 1.0, league_avg=1.35)
    assert result["attack_strength"] > 1.0


def test_xg_ratio_below_average():
    result = compute_xg_ratio(0.8, 1.5, league_avg=1.35)
    assert result["attack_strength"] < 1.0


def test_add_xg_features_columns():
    df = pd.DataFrame({
        "team": ["Arsenal", "Chelsea"],
        "avg_goals_5": [1.8, 1.2],
        "avg_goals_against_5": [0.8, 1.5],
    })
    result = add_xg_features(df)
    assert "attack_strength" in result.columns
    assert "defence_strength" in result.columns
    assert "xg_ratio" in result.columns


def test_add_xg_features_values():
    df = pd.DataFrame({"team": ["Arsenal"], "avg_goals_5": [1.35], "avg_goals_against_5": [1.35]})
    result = add_xg_features(df, league_avg_goals=1.35)
    assert result["attack_strength"].iloc[0] == pytest.approx(1.0)
