import pandas as pd
import pytest
from league_strength import goals_per_match_by_league, home_advantage_by_league, league_strength_report


@pytest.fixture
def matches():
    return pd.DataFrame({
        "league": ["PL", "PL", "PD", "PD"],
        "homeTeam": ["A", "C", "E", "G"],
        "awayTeam": ["B", "D", "F", "H"],
        "homeScore": [3, 1, 2, 0],
        "awayScore": [1, 1, 0, 2],
    })


def test_goals_per_match(matches):
    result = goals_per_match_by_league(matches)
    assert "PL" in result.index
    assert result["PL"] == pytest.approx((4 + 2) / 2)


def test_home_advantage(matches):
    ha = home_advantage_by_league(matches)
    assert 0 <= ha["PL"] <= 1


def test_league_strength_report_columns(matches):
    report = league_strength_report(matches)
    assert "avg_goals_per_match" in report.columns
    assert "home_win_rate" in report.columns
    assert "competitive_balance" in report.columns
