import pandas as pd
import pytest
from analytics import compute_roi, compute_win_rate, cumulative_pnl, by_prediction


@pytest.fixture
def sample_bets():
    return pd.DataFrame({
        "match": ["A vs B", "C vs D", "E vs F", "G vs H"],
        "prediction": ["Home Win", "Away Win", "Home Win", "Draw"],
        "stake": [100.0, 50.0, 80.0, 60.0],
        "pnl": [100.0, -50.0, 80.0, -60.0],
        "won": [True, False, True, False],
        "league": ["PL", "PD", "PL", "SA"],
    })


def test_compute_roi(sample_bets):
    roi = compute_roi(sample_bets)
    expected = (100 - 50 + 80 - 60) / (100 + 50 + 80 + 60)
    assert roi == pytest.approx(expected)


def test_compute_win_rate(sample_bets):
    assert compute_win_rate(sample_bets) == 0.5


def test_compute_roi_empty():
    assert compute_roi(pd.DataFrame()) is None


def test_compute_win_rate_empty():
    assert compute_win_rate(pd.DataFrame()) is None


def test_cumulative_pnl(sample_bets):
    cum = cumulative_pnl(sample_bets)
    assert cum.iloc[-1] == pytest.approx(70.0)


def test_by_prediction(sample_bets):
    result = by_prediction(sample_bets)
    assert "Home Win" in result.index
    assert result.loc["Home Win", "bets_count"] == 2
