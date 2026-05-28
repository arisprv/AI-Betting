import pytest
from bankroll import BankrollManager


def test_initial_capital():
    bm = BankrollManager(initial_capital=500.0)
    assert bm.current_capital == 500.0


def test_kelly_stake_positive_edge():
    bm = BankrollManager(initial_capital=1000.0)
    stake = bm.kelly_stake(prob=0.6, odds=2.0)
    assert stake > 0


def test_kelly_stake_no_edge():
    bm = BankrollManager(initial_capital=1000.0)
    stake = bm.kelly_stake(prob=0.4, odds=2.0)
    assert stake == 0.0


def test_kelly_stake_capped_at_10_percent():
    bm = BankrollManager(initial_capital=1000.0)
    stake = bm.kelly_stake(prob=0.99, odds=10.0)
    assert stake <= 100.0


def test_record_bet_win():
    bm = BankrollManager(initial_capital=1000.0)
    pnl = bm.record_bet("A vs B", "Home Win", stake=50.0, odds=2.0, won=True)
    assert pnl == 50.0
    assert bm.current_capital == 1050.0


def test_record_bet_loss():
    bm = BankrollManager(initial_capital=1000.0)
    pnl = bm.record_bet("A vs B", "Home Win", stake=50.0, odds=2.0, won=False)
    assert pnl == -50.0
    assert bm.current_capital == 950.0


def test_roi_calculation():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", stake=100.0, odds=2.0, won=True)
    bm.record_bet("C vs D", "Away Win", stake=100.0, odds=2.0, won=False)
    assert bm.roi == pytest.approx(0.0, abs=1e-6)


def test_win_rate():
    bm = BankrollManager(initial_capital=1000.0)
    bm.record_bet("A vs B", "Home Win", stake=50.0, odds=2.0, won=True)
    bm.record_bet("C vs D", "Away Win", stake=50.0, odds=2.0, won=False)
    assert bm.win_rate == 0.5


def test_empty_win_rate():
    bm = BankrollManager()
    assert bm.win_rate is None
