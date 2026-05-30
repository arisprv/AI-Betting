import pandas as pd
import pytest
from trend_analyzer import rolling_win_rate, performance_trend


@pytest.fixture
def matches_improving():
    """Team wins more and more over time."""
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=10, freq="7D"),
        "homeTeam": ["Arsenal"] * 10,
        "awayTeam": [f"Team{i}" for i in range(10)],
        "homeScore": [0, 0, 1, 1, 2, 2, 2, 3, 3, 3],
        "awayScore": [2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    })


@pytest.fixture
def matches_stable():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "homeTeam": ["Arsenal"] * 6,
        "awayTeam": [f"Team{i}" for i in range(6)],
        "homeScore": [2, 1, 2, 1, 2, 1],
        "awayScore": [0, 1, 0, 1, 0, 1],
    })


def test_rolling_win_rate_length(matches_stable):
    rates = rolling_win_rate(matches_stable, "Arsenal", window=3)
    assert len(rates) == 6


def test_rolling_win_rate_range(matches_stable):
    rates = rolling_win_rate(matches_stable, "Arsenal", window=3)
    assert all(0 <= r <= 1 for r in rates)


def test_performance_trend_improving(matches_improving):
    trend = performance_trend(matches_improving, "Arsenal")
    assert trend == "improving"


def test_performance_trend_stable(matches_stable):
    trend = performance_trend(matches_stable, "Arsenal")
    assert trend in ("stable", "improving", "declining")
