import pandas as pd
import pytest
from team_profile import build_team_profile, compare_teams


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Spurs", "Liverpool", "Everton"],
        "homeScore": [2, 1, 1, 3, 0, 2],
        "awayScore": [0, 1, 2, 0, 1, 1],
    })


def test_build_team_profile_keys(matches):
    profile = build_team_profile(matches, "Arsenal")
    assert "form_points" in profile
    assert "form_string" in profile
    assert "unbeaten_streak" in profile
    assert "winning_streak" in profile
    assert "goal_trend" in profile


def test_build_team_profile_team_name(matches):
    profile = build_team_profile(matches, "Arsenal")
    assert profile["team"] == "Arsenal"


def test_compare_teams_structure(matches):
    result = compare_teams(matches, "Arsenal", "Chelsea")
    assert "home" in result
    assert "away" in result
    assert result["home"]["team"] == "Arsenal"
    assert result["away"]["team"] == "Chelsea"
