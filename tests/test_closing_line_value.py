import pytest
from closing_line_value import clv, average_clv, interpret_clv


def test_clv_positive_when_odds_drift_out():
    # Opening 2.0, closing 2.2 — closing shorter, so CLV negative
    # Opening 2.2, closing 2.0 — you got better than closing, CLV positive
    result = clv(opening_odds=2.2, closing_odds=2.0)
    assert result > 0


def test_clv_negative_when_odds_shorten():
    result = clv(opening_odds=2.0, closing_odds=2.2)
    assert result < 0


def test_clv_zero_for_same_odds():
    assert clv(2.0, 2.0) == pytest.approx(0.0)


def test_clv_invalid_odds():
    assert clv(0, 2.0) == 0.0
    assert clv(2.0, 0) == 0.0


def test_average_clv_empty():
    assert average_clv([]) == 0.0


def test_average_clv_values():
    result = average_clv([2.0, -1.0, 3.0])
    assert result == pytest.approx(4 / 3)


def test_interpret_clv_excellent():
    assert "Excellent" in interpret_clv(5.0)


def test_interpret_clv_poor():
    assert "Poor" in interpret_clv(-3.0)
