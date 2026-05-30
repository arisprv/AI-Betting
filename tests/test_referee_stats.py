import pandas as pd
import pytest
from referee_stats import home_bias_score


@pytest.fixture
def matches():
    return pd.DataFrame({
        "referee": ["Smith", "Jones", "Smith", "Jones"],
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Liverpool"],
        "awayTeam": ["Chelsea", "Arsenal", "Liverpool", "Arsenal"],
        "homeScore": [2, 1, 3, 0],
        "awayScore": [0, 0, 0, 2],
    })


def test_home_bias_score_keys(matches):
    result = home_bias_score(matches)
    assert "Smith" in result.index
    assert "Jones" in result.index


def test_home_bias_score_range(matches):
    result = home_bias_score(matches)
    for val in result:
        assert 0.0 <= val <= 1.0


def test_home_bias_missing_referee_column():
    df = pd.DataFrame({"homeTeam": ["A"], "awayTeam": ["B"], "homeScore": [1], "awayScore": [0]})
    result = home_bias_score(df)
    assert result.empty
