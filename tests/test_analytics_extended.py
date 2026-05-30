import pandas as pd
import pytest
from analytics import sharpe_ratio_bets, max_drawdown_bets


@pytest.fixture
def bets():
    return pd.DataFrame({
        "stake": [50.0, 50.0, 50.0, 50.0],
        "pnl": [50.0, -50.0, 50.0, -50.0],
        "balance": [1050.0, 1000.0, 1050.0, 1000.0],
    })


def test_sharpe_ratio_bets_value(bets):
    sr = sharpe_ratio_bets(bets)
    assert sr is None or isinstance(sr, float)


def test_max_drawdown_bets_range(bets):
    dd = max_drawdown_bets(bets)
    assert 0.0 <= dd <= 1.0


def test_max_drawdown_monotone_increase():
    bets = pd.DataFrame({"balance": [1000, 1050, 1100, 1150]})
    assert max_drawdown_bets(bets) == pytest.approx(0.0)


def test_max_drawdown_after_drop():
    bets = pd.DataFrame({"balance": [1000, 1200, 900, 1100]})
    dd = max_drawdown_bets(bets)
    assert dd == pytest.approx((1200 - 900) / 1200)
