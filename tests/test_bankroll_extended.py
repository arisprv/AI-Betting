import pytest
from bankroll import BankrollManager


def test_profit_after_win():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", 50.0, 2.0, True)
    assert bm.profit == pytest.approx(50.0)


def test_profit_after_loss():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", 50.0, 2.0, False)
    assert bm.profit == pytest.approx(-50.0)


def test_max_drawdown_after_losses():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", 100.0, 2.0, False)  # down to 900
    bm.record_bet("C vs D", "Draw", 100.0, 2.0, False)       # down to 800
    assert bm.max_drawdown == pytest.approx(0.2)


def test_max_drawdown_zero_no_losses():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", 50.0, 2.0, True)
    assert bm.max_drawdown == pytest.approx(0.0)


def test_summary_keys():
    bm = BankrollManager(initial_capital=1000.0)
    s = bm.summary()
    assert "initial" in s and "current" in s and "roi" in s and "max_drawdown" in s
