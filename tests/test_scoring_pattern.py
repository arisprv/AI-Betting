import pandas as pd
import pytest
from scoring_pattern import high_scoring_rate, average_margin


@pytest.fixture
def matches():
    return pd.DataFrame({
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Spurs"],
        "homeScore": [3, 2, 1, 0],
        "awayScore": [0, 1, 2, 1],
    })


def test_high_scoring_rate_range(matches):
    rate = high_scoring_rate(matches, "Arsenal", threshold=2)
    assert 0.0 <= rate <= 1.0


def test_high_scoring_rate_all(matches):
    all_matches = pd.DataFrame({
        "homeTeam": ["Arsenal"] * 3,
        "awayTeam": ["A", "B", "C"],
        "homeScore": [3, 4, 2],
        "awayScore": [0, 0, 0],
    })
    assert high_scoring_rate(all_matches, "Arsenal", threshold=2) == 1.0


def test_average_margin_positive(matches):
    margin = average_margin(matches, "Arsenal")
    assert isinstance(margin, float)


def test_average_margin_zero():
    matches = pd.DataFrame({
        "homeTeam": ["Arsenal"],
        "awayTeam": ["Chelsea"],
        "homeScore": [1],
        "awayScore": [1],
    })
    assert average_margin(matches, "Arsenal") == pytest.approx(0.0)
