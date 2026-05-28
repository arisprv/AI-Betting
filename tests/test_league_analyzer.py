import pandas as pd
import pytest
from league_analyzer import home_advantage, avg_goals_per_match, btts_rate_by_league, over_under_rate


@pytest.fixture
def matches():
    return pd.DataFrame({
        "league": ["PL", "PL", "PL", "PD", "PD"],
        "homeTeam": ["A", "C", "E", "G", "I"],
        "awayTeam": ["B", "D", "F", "H", "J"],
        "homeScore": [2, 1, 0, 3, 2],
        "awayScore": [1, 1, 2, 1, 0],
    })


def test_home_advantage(matches):
    ha = home_advantage(matches)
    assert "PL" in ha.index
    assert 0 <= ha["PL"] <= 1


def test_avg_goals(matches):
    avg = avg_goals_per_match(matches)
    assert avg["PL"] == pytest.approx((3 + 2 + 2) / 3)


def test_btts_rate(matches):
    btts = btts_rate_by_league(matches)
    assert btts["PL"] == pytest.approx(1 / 3)


def test_over_under(matches):
    ou = over_under_rate(matches, threshold=2.5)
    assert 0 <= ou["PL"] <= 1
