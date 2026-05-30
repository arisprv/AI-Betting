import pytest
from risk_metrics import sharpe_ratio, expectancy


def test_sharpe_negative_returns():
    returns = [-0.05, -0.10, -0.08, -0.06]
    sr = sharpe_ratio(returns)
    assert sr is not None
    assert sr < 0


def test_sharpe_zero_risk_free():
    returns = [0.1, 0.2, 0.15, 0.05]
    sr = sharpe_ratio(returns, risk_free_rate=0.0)
    assert sr is not None and sr > 0


def test_expectancy_no_wins():
    ev = expectancy(wins=0, losses=10, avg_win=20.0, avg_loss=10.0)
    assert ev < 0


def test_expectancy_no_losses():
    ev = expectancy(wins=10, losses=0, avg_win=20.0, avg_loss=10.0)
    assert ev == pytest.approx(20.0)


def test_expectancy_balanced():
    ev = expectancy(wins=5, losses=5, avg_win=20.0, avg_loss=20.0)
    assert ev == pytest.approx(0.0)
