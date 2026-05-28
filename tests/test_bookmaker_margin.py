import pytest
from bookmaker_margin import overround, true_probabilities, margin_percent, fair_odds


def test_overround_positive():
    margin = overround(2.0, 3.5, 4.0)
    assert margin > 0


def test_overround_fair_market():
    margin = overround(2.0, 4.0, 4.0)
    assert margin == pytest.approx(0.0, abs=0.05)


def test_true_probabilities_sum_to_one():
    probs = true_probabilities(2.0, 3.5, 4.0)
    assert abs(sum(probs.values()) - 1.0) < 1e-9


def test_true_probabilities_keys():
    probs = true_probabilities(2.0, 3.5, 4.0)
    assert set(probs.keys()) == {"Home Win", "Draw", "Away Win"}


def test_margin_percent():
    pct = margin_percent(1.9, 3.4, 4.0)
    assert pct > 0
    assert pct < 20


def test_fair_odds_returns_dict():
    odds = fair_odds(2.0, 3.5, 4.0)
    assert isinstance(odds, dict)
    assert all(v > 0 for v in odds.values())
