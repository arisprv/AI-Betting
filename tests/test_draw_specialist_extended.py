import pandas as pd
import pytest
from draw_specialist import top_draw_teams


@pytest.fixture
def matches():
    return pd.DataFrame({
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Chelsea", "Arsenal", "Arsenal", "Liverpool"],
        "homeScore": [1, 2, 1, 0, 1],
        "awayScore": [1, 1, 1, 0, 1],
    })


def test_top_draw_teams_returns_df(matches):
    result = top_draw_teams(matches, n=3)
    assert isinstance(result, pd.DataFrame)


def test_top_draw_teams_sorted(matches):
    result = top_draw_teams(matches, n=10)
    rates = result["draw_rate"].tolist()
    assert rates == sorted(rates, reverse=True)


def test_top_draw_teams_count(matches):
    result = top_draw_teams(matches, n=2)
    assert len(result) <= 2
