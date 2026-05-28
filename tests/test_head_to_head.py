import pandas as pd
import pytest
from head_to_head import get_h2h_stats, enrich_with_h2h


@pytest.fixture
def matches():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=4, freq="30D"),
        "homeTeam": ["Arsenal", "Chelsea", "Arsenal", "Chelsea"],
        "awayTeam": ["Chelsea", "Arsenal", "Chelsea", "Arsenal"],
        "homeScore": [2, 1, 0, 2],
        "awayScore": [1, 1, 2, 0],
    })


def test_h2h_count(matches):
    stats = get_h2h_stats(matches, "Arsenal", "Chelsea", n=10)
    assert stats["h2h_count"] == 4


def test_h2h_rates_sum_to_one(matches):
    stats = get_h2h_stats(matches, "Arsenal", "Chelsea", n=10)
    total = stats["h2h_home_wins"] + stats["h2h_draws"] + stats["h2h_away_wins"]
    assert total == pytest.approx(1.0)


def test_h2h_no_matches():
    empty = pd.DataFrame(columns=["date", "homeTeam", "awayTeam", "homeScore", "awayScore"])
    stats = get_h2h_stats(empty, "A", "B")
    assert stats["h2h_count"] == 0


def test_enrich_with_h2h(matches):
    upcoming = pd.DataFrame({"homeTeam": ["Arsenal"], "awayTeam": ["Chelsea"]})
    enriched = enrich_with_h2h(upcoming, matches)
    assert "h2h_count" in enriched.columns
    assert enriched["h2h_count"].iloc[0] == 4
