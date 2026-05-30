import pandas as pd
import pytest
from season_stats import team_season_stats


@pytest.fixture
def perfect_season():
    """Team wins every home game, loses every away game."""
    return pd.DataFrame({
        "homeTeam": ["Arsenal"] * 5,
        "awayTeam": ["A", "B", "C", "D", "E"],
        "homeScore": [2, 3, 1, 4, 2],
        "awayScore": [0, 0, 0, 0, 0],
    })


def test_perfect_home_season_points(perfect_season):
    stats = team_season_stats(perfect_season, "Arsenal")
    assert stats["played"] == 5
    assert stats["goals_scored"] == 12
    assert stats["goals_conceded"] == 0
    assert stats["goal_diff"] == 12


def test_no_matches_returns_zeros():
    empty = pd.DataFrame({"homeTeam": [], "awayTeam": [], "homeScore": [], "awayScore": []})
    stats = team_season_stats(empty, "Arsenal")
    assert stats["played"] == 0
    assert stats["goals_scored"] == 0
