import pandas as pd
import pytest
from season_stats import team_season_stats, league_season_summary


@pytest.fixture
def matches():
    return pd.DataFrame({
        "league": ["PL"] * 5,
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal", "Chelsea"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Spurs", "Liverpool"],
        "homeScore": [2, 1, 1, 3, 0],
        "awayScore": [0, 1, 2, 0, 2],
    })


def test_team_season_stats_keys(matches):
    stats = team_season_stats(matches, "Arsenal")
    assert "played" in stats
    assert "goals_scored" in stats
    assert "points" in stats


def test_team_season_stats_played(matches):
    stats = team_season_stats(matches, "Arsenal")
    assert stats["played"] == 4


def test_team_season_stats_goals(matches):
    stats = team_season_stats(matches, "Arsenal")
    assert stats["goals_scored"] == 2 + 1 + 3 + 2  # home + away scored


def test_league_summary_columns(matches):
    summary = league_season_summary(matches)
    assert "league" in summary.columns
    assert "avg_goals" in summary.columns


def test_league_summary_row_count(matches):
    summary = league_season_summary(matches)
    assert len(summary) == 1  # only PL
