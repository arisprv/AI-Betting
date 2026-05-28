import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock
from backtester import run_backtest
from constants import RESULT_HOME_WIN


FEATURE_COLS = [
    "home_avg_goals_for_5", "home_avg_goals_against_5", "home_win_rate_5",
    "away_avg_goals_for_5", "away_avg_goals_against_5", "away_win_rate_5",
]


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.classes_ = np.array([-1, 0, 1])
    model.predict_proba = MagicMock(return_value=np.array([[0.1, 0.2, 0.7]]))
    return model


@pytest.fixture
def sample_data():
    matches = pd.DataFrame({
        "utcDate": pd.date_range("2025-02-01", periods=3, freq="7D"),
        "homeTeam": ["Arsenal", "Chelsea", "Liverpool"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal"],
        "homeScore": [2, 1, 0],
        "awayScore": [0, 1, 1],
        "result": [RESULT_HOME_WIN, 0, -1],
    })
    features = pd.DataFrame({
        "utcDate": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "team": ["Arsenal", "Arsenal", "Chelsea", "Chelsea", "Liverpool", "Liverpool"],
        "is_home": [True, True, False, False, True, True],
        "avg_goals_5": [1.8, 1.8, 1.2, 1.2, 1.5, 1.5],
        "avg_goals_against_5": [0.8, 0.8, 1.4, 1.4, 1.0, 1.0],
        "win_rate_5": [0.7, 0.7, 0.4, 0.4, 0.5, 0.5],
    })
    return matches, features


def test_backtest_returns_bankroll(mock_model, sample_data):
    matches, features = sample_data
    bankroll, bets = run_backtest(matches, features, mock_model, FEATURE_COLS, confidence_threshold=0.6)
    assert bankroll is not None


def test_backtest_bets_dataframe(mock_model, sample_data):
    matches, features = sample_data
    _, bets = run_backtest(matches, features, mock_model, FEATURE_COLS, confidence_threshold=0.6)
    if not bets.empty:
        assert "match" in bets.columns
        assert "confidence" in bets.columns
