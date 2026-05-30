import pandas as pd
import pytest
from fixture_difficulty import average_difficulty


def test_average_difficulty_empty():
    df = pd.DataFrame()
    result = average_difficulty(df, col="opp_elo")
    assert result == 0.0


def test_average_difficulty_value():
    df = pd.DataFrame({"opp_elo": [1500, 1600, 1400]})
    result = average_difficulty(df, col="opp_elo")
    assert result == pytest.approx(1500.0)


def test_average_difficulty_missing_col():
    df = pd.DataFrame({"some_col": [1, 2, 3]})
    result = average_difficulty(df, col="opp_elo")
    assert result == 0.0
