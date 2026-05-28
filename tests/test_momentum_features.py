import pandas as pd
import pytest
from momentum_features import goal_trend, unbeaten_streak, winning_streak


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=5, freq="7D"),
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Arsenal", "Arsenal"],
        "awayTeam": ["Chelsea", "Arsenal", "Liverpool", "Spurs", "Everton"],
        "homeScore": [1, 0, 2, 3, 4],
        "awayScore": [0, 1, 0, 0, 0],
    })


def test_goal_trend_increasing(matches):
    trend = goal_trend(matches, "Arsenal")
    assert trend >= 0


def test_unbeaten_streak(matches):
    streak = unbeaten_streak(matches, "Arsenal")
    assert isinstance(streak, int)
    assert streak >= 0


def test_winning_streak(matches):
    streak = winning_streak(matches, "Arsenal")
    assert streak >= 0


def test_unbeaten_streak_after_loss():
    matches = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=3, freq="7D"),
        "homeTeam": ["Arsenal", "Arsenal", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Spurs"],
        "homeScore": [0, 2, 1],
        "awayScore": [2, 0, 0],
    })
    streak = unbeaten_streak(matches, "Arsenal")
    assert streak == 2


def test_winning_streak_zero():
    matches = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=2, freq="7D"),
        "homeTeam": ["Arsenal", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool"],
        "homeScore": [0, 0],
        "awayScore": [1, 1],
    })
    assert winning_streak(matches, "Arsenal") == 0
