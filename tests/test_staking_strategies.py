import pytest
from staking_strategies import flat_stake, percentage_stake, kelly_stake, fibonacci_stake, d_alembert_stake


def test_flat_stake():
    assert flat_stake(1000, unit_size=10) == 10.0


def test_flat_stake_capped_by_bankroll():
    assert flat_stake(5.0, unit_size=10) == 5.0


def test_percentage_stake():
    result = percentage_stake(1000, pct=0.02)
    assert result == pytest.approx(20.0)


def test_kelly_stake_positive_edge():
    stake = kelly_stake(1000, prob=0.6, odds=2.0)
    assert stake > 0


def test_kelly_stake_no_edge():
    stake = kelly_stake(1000, prob=0.4, odds=2.0)
    assert stake == 0.0


def test_kelly_stake_capped():
    stake = kelly_stake(1000, prob=0.99, odds=10.0)
    assert stake <= 100.0


def test_fibonacci_stake_zero_streak():
    stake = fibonacci_stake(1000, loss_streak=0, base_unit=10)
    assert stake == pytest.approx(10.0)


def test_fibonacci_stake_increases_with_losses():
    s0 = fibonacci_stake(1000, loss_streak=0, base_unit=10)
    s3 = fibonacci_stake(1000, loss_streak=3, base_unit=10)
    assert s3 > s0


def test_d_alembert_stake_even():
    stake = d_alembert_stake(1000, wins=2, losses=2, base_unit=10)
    assert stake == pytest.approx(10.0)
