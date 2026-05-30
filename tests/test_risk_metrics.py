import pytest
from risk_metrics import sharpe_ratio, max_drawdown, expectancy, profit_factor, recovery_factor


def test_sharpe_positive_returns():
    returns = [0.05, 0.10, 0.08, 0.06, 0.09]
    sr = sharpe_ratio(returns)
    assert sr is not None and sr > 0


def test_sharpe_insufficient_data():
    assert sharpe_ratio([0.05]) is None


def test_sharpe_zero_variance():
    assert sharpe_ratio([0.05, 0.05, 0.05]) is None


def test_max_drawdown_none():
    assert max_drawdown([]) == 0.0


def test_max_drawdown_monotone_increase():
    assert max_drawdown([100, 110, 120, 130]) == pytest.approx(0.0)


def test_max_drawdown_with_drop():
    dd = max_drawdown([100, 120, 90, 110])
    assert dd == pytest.approx((120 - 90) / 120)


def test_expectancy_positive():
    ev = expectancy(wins=6, losses=4, avg_win=15.0, avg_loss=10.0)
    assert ev > 0


def test_expectancy_zero():
    ev = expectancy(wins=0, losses=0, avg_win=10.0, avg_loss=10.0)
    assert ev == 0.0


def test_profit_factor():
    pf = profit_factor(300, 200)
    assert pf == pytest.approx(1.5)


def test_profit_factor_zero_loss():
    assert profit_factor(100, 0) is None


def test_recovery_factor():
    assert recovery_factor(500, 100) == pytest.approx(5.0)
