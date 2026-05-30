import pandas as pd
import pytest
from performance_dashboard import build_dashboard


@pytest.fixture
def bets():
    return pd.DataFrame({
        "match": ["A vs B", "C vs D", "E vs F"],
        "prediction": ["Home Win", "Away Win", "Draw"],
        "stake": [50.0, 30.0, 40.0],
        "pnl": [40.0, -30.0, 30.0],
        "won": [True, False, True],
        "balance": [1040.0, 1010.0, 1040.0],
        "league": ["PL", "PD", "PL"],
    })


def test_dashboard_keys(bets):
    d = build_dashboard(bets)
    assert "total_bets" in d
    assert "roi_pct" in d
    assert "win_rate_pct" in d
    assert "max_drawdown_pct" in d


def test_dashboard_total_bets(bets):
    d = build_dashboard(bets)
    assert d["total_bets"] == 3


def test_dashboard_empty():
    d = build_dashboard(pd.DataFrame())
    assert d == {}


def test_dashboard_win_rate(bets):
    d = build_dashboard(bets)
    assert abs(d["win_rate_pct"] - (2 / 3 * 100)) < 1.0
