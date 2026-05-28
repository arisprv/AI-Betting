import pandas as pd
import pytest
from position_tracker import build_table, get_position


@pytest.fixture
def matches():
    return pd.DataFrame({
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Liverpool"],
        "homeScore": [3, 1, 2],
        "awayScore": [0, 1, 0],
    })


def test_table_columns(matches):
    table = build_table(matches)
    assert "team" in table.columns
    assert "points" in table.columns
    assert "gd" in table.columns


def test_table_size(matches):
    table = build_table(matches)
    assert len(table) == 3


def test_table_sorted_by_points(matches):
    table = build_table(matches)
    points = table["points"].tolist()
    assert points == sorted(points, reverse=True)


def test_arsenal_is_first(matches):
    table = build_table(matches)
    assert table.iloc[0]["team"] == "Arsenal"


def test_get_position(matches):
    table = build_table(matches)
    pos = get_position(table, "Arsenal")
    assert pos == 1


def test_get_position_missing(matches):
    table = build_table(matches)
    assert get_position(table, "Nonexistent FC") == -1
