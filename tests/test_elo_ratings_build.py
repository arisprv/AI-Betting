import pandas as pd
import pytest
from elo_ratings import build_elo_ratings, DEFAULT_RATING


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=4, freq="7D"),
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Liverpool"],
        "awayTeam": ["Chelsea", "Liverpool", "Liverpool", "Arsenal"],
        "homeScore": [2, 1, 3, 0],
        "awayScore": [1, 2, 0, 1],
    })


def test_all_teams_present(matches):
    ratings = build_elo_ratings(matches)
    assert "Arsenal" in ratings
    assert "Chelsea" in ratings
    assert "Liverpool" in ratings


def test_ratings_are_floats(matches):
    ratings = build_elo_ratings(matches)
    for team, rating in ratings.items():
        assert isinstance(rating, float)


def test_winner_gains_rating(matches):
    ratings = build_elo_ratings(matches)
    assert ratings["Arsenal"] > DEFAULT_RATING or ratings["Chelsea"] < DEFAULT_RATING


def test_default_rating_applied():
    empty_matches = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=1),
        "homeTeam": ["Arsenal"],
        "awayTeam": ["Chelsea"],
        "homeScore": [1],
        "awayScore": [0],
    })
    ratings = build_elo_ratings(empty_matches)
    assert len(ratings) == 2
