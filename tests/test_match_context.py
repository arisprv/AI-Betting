import pandas as pd
import pytest
from match_context import days_since_last_match, is_high_rest_advantage, matches_in_last_n_days, fatigue_index


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=5, freq="7D"),
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal", "Chelsea"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Spurs", "Liverpool"],
        "homeScore": [2, 1, 1, 3, 0],
        "awayScore": [1, 1, 1, 0, 2],
    })


def test_days_since_last_match(matches):
    days = days_since_last_match(matches, "Arsenal", "2025-02-01")
    assert days > 0


def test_days_since_no_match():
    empty = pd.DataFrame(columns=["date", "homeTeam", "awayTeam"])
    days = days_since_last_match(empty, "Arsenal", "2025-02-01")
    assert days == 7


def test_high_rest_advantage_true():
    assert is_high_rest_advantage(7, 3, threshold=3) is True


def test_high_rest_advantage_false():
    assert is_high_rest_advantage(5, 5, threshold=3) is False


def test_matches_in_last_n_days(matches):
    count = matches_in_last_n_days(matches, "Arsenal", "2025-02-01", n=40)
    assert count >= 0


def test_fatigue_index():
    assert fatigue_index(4, 2) == pytest.approx(2.0)
    assert fatigue_index(0, 7) == pytest.approx(0.0)
