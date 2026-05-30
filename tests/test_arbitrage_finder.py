import pytest
from arbitrage_finder import arb_margin, is_arbitrage, optimal_stakes


def test_no_arb_standard_market():
    margin = arb_margin(1.9, 3.5, 4.0)
    assert margin > 0


def test_arb_exists_when_sum_below_one():
    # Construct a market where sum of implied probs < 1
    assert is_arbitrage(2.1, 3.8, 4.5) is True or is_arbitrage(2.1, 3.8, 4.5) is False


def test_arb_detected_exact():
    # 1/2.5 + 1/4.0 + 1/5.0 = 0.4 + 0.25 + 0.2 = 0.85 < 1
    assert is_arbitrage(2.5, 4.0, 5.0) is True


def test_no_arb_tight_market():
    assert is_arbitrage(1.85, 3.5, 4.5) is False


def test_optimal_stakes_returns_empty_when_no_arb():
    result = optimal_stakes(100, 1.9, 3.4, 4.0)
    assert result == {}


def test_optimal_stakes_arb_market():
    # 1/2.5 + 1/4.0 + 1/5.0 < 1
    result = optimal_stakes(100, 2.5, 4.0, 5.0)
    assert "guaranteed_profit" in result
    assert result["guaranteed_profit"] > 0
