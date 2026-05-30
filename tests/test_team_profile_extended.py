import pandas as pd
import pytest
from team_profile import build_team_profile


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=8, freq="7D"),
        "homeTeam": ["Arsenal"] * 5 + ["Chelsea", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Spurs", "Everton", "West Ham",
                     "Arsenal", "Liverpool", "Chelsea"],
        "homeScore": [3, 2, 0, 1, 2, 1, 0, 2],
        "awayScore": [0, 1, 1, 0, 0, 2, 1, 1],
    })


def test_profile_form_string_length(matches):
    profile = build_team_profile(matches, "Arsenal", window=5)
    assert len(profile["form_string"]) <= 5


def test_profile_goal_trend_type(matches):
    profile = build_team_profile(matches, "Arsenal", window=5)
    assert isinstance(profile["goal_trend"], float)


def test_profile_high_scoring_range(matches):
    profile = build_team_profile(matches, "Arsenal", window=5)
    assert 0.0 <= profile["high_scoring_rate"] <= 1.0
