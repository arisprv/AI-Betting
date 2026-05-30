import pandas as pd
import pytest
from draw_specialist import team_draw_rate, h2h_draw_rate, draw_probability_indicator


@pytest.fixture
def matches():
    return pd.DataFrame({
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Spurs"],
        "homeScore": [1, 1, 1, 2],
        "awayScore": [1, 1, 1, 0],
    })


def test_team_draw_rate_range(matches):
    rate = team_draw_rate(matches, "Arsenal")
    assert 0.0 <= rate <= 1.0


def test_team_draw_rate_all_draws():
    df = pd.DataFrame({
        "homeTeam": ["Arsenal"] * 3,
        "awayTeam": ["A", "B", "C"],
        "homeScore": [1, 1, 1],
        "awayScore": [1, 1, 1],
    })
    assert team_draw_rate(df, "Arsenal") == pytest.approx(1.0)


def test_h2h_draw_rate(matches):
    rate = h2h_draw_rate(matches, "Arsenal", "Chelsea")
    assert 0.0 <= rate <= 1.0


def test_h2h_draw_rate_no_matches():
    empty = pd.DataFrame(columns=["homeTeam", "awayTeam", "homeScore", "awayScore"])
    assert h2h_draw_rate(empty, "A", "B") == 0.0


def test_draw_probability_indicator():
    result = draw_probability_indicator(0.3, 0.4, 0.5)
    assert 0.0 <= result <= 1.0
