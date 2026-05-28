import pandas as pd
import pytest
from form_calculator import recent_form_points, form_string, get_result, POINTS_MAP


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=5, freq="7D"),
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Liverpool", "Arsenal"],
        "awayTeam": ["Chelsea", "Arsenal", "Liverpool", "Arsenal", "Chelsea"],
        "homeScore": [2, 1, 0, 2, 3],
        "awayScore": [1, 1, 2, 0, 1],
    })


def test_get_result_home_win():
    assert get_result(2, 1, "home") == 1


def test_get_result_draw():
    assert get_result(1, 1, "home") == 0


def test_get_result_away_win():
    assert get_result(0, 2, "away") == 1


def test_recent_form_points_arsenal(matches):
    points = recent_form_points(matches, "Arsenal", n=5)
    assert isinstance(points, int)
    assert 0 <= points <= 15


def test_form_string_length(matches):
    s = form_string(matches, "Arsenal", n=3)
    assert len(s) == 3
    assert all(c in "WDL" for c in s)


def test_form_string_all_wins():
    matches = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=3, freq="7D"),
        "homeTeam": ["Arsenal"] * 3,
        "awayTeam": ["Chelsea", "Liverpool", "Spurs"],
        "homeScore": [3, 2, 1],
        "awayScore": [0, 0, 0],
    })
    assert form_string(matches, "Arsenal", n=3) == "WWW"
