import pandas as pd
import pytest
from market_efficiency import market_efficiency_score, model_vs_market


@pytest.fixture
def odds_df():
    return pd.DataFrame({
        "home_team": ["Arsenal"],
        "away_team": ["Chelsea"],
        "home_odds": [2.0],
        "draw_odds": [3.5],
        "away_odds": [4.0],
    })


def test_market_efficiency_score_length(odds_df):
    scores = market_efficiency_score(odds_df)
    assert len(scores) == 1


def test_market_efficiency_score_positive(odds_df):
    scores = market_efficiency_score(odds_df)
    assert scores.iloc[0] > 0


def test_model_vs_market_is_value():
    result = model_vs_market(0.6, 2.0, 3.5, 4.0, "Home Win")
    assert "edge" in result
    assert "is_value" in result
    assert result["is_value"] == (result["edge"] > 0)


def test_model_vs_market_no_value():
    result = model_vs_market(0.3, 2.0, 3.5, 4.0, "Home Win")
    # Model prob 0.3 vs implied prob ~0.44 → no value
    assert result["is_value"] is False
