import pandas as pd
import pytest
from season_predictor import predict_title_odds


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Liverpool", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Arsenal", "Liverpool", "Arsenal", "Liverpool", "Spurs"],
        "homeScore": [2, 1, 1, 0, 2, 3],
        "awayScore": [0, 2, 1, 1, 0, 0],
    })


def test_predict_title_odds_returns_df(matches):
    teams = ["Arsenal", "Chelsea", "Liverpool", "Spurs"]
    result = predict_title_odds(matches, pd.DataFrame(), teams, n_sims=50)
    assert isinstance(result, pd.DataFrame)


def test_predict_title_probs_sum_to_one(matches):
    teams = ["Arsenal", "Chelsea", "Liverpool"]
    result = predict_title_odds(matches, pd.DataFrame(), teams, n_sims=100)
    assert abs(result["title_prob"].sum() - 1.0) < 0.01


def test_predict_title_has_all_teams(matches):
    teams = ["Arsenal", "Chelsea", "Liverpool"]
    result = predict_title_odds(matches, pd.DataFrame(), teams, n_sims=50)
    assert set(result["team"]) == set(teams)
