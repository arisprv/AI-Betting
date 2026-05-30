import pytest
from staking_strategies import percentage_stake, proportional_kelly


def test_percentage_stake_scales_with_bankroll():
    small = percentage_stake(500, pct=0.02)
    large = percentage_stake(2000, pct=0.02)
    assert large == pytest.approx(small * 4)


def test_proportional_kelly_less_than_full():
    full = pytest.approx
    pk = proportional_kelly(1000, prob=0.6, odds=2.0, kelly_pct=0.5)
    from staking_strategies import kelly_stake
    full_k = kelly_stake(1000, prob=0.6, odds=2.0, fraction=0.25)
    assert pk <= full_k


def test_percentage_zero_bankroll():
    assert percentage_stake(0, pct=0.05) == 0.0
