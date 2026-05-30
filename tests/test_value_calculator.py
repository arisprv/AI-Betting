import pytest
from value_calculator import composite_value_score


def test_value_detected_with_strong_edge():
    result = composite_value_score(0.65, 2.0, 3.5, 4.0, "Home Win")
    assert result["is_value"] is True


def test_no_value_with_low_prob():
    result = composite_value_score(0.30, 2.0, 3.5, 4.0, "Home Win")
    assert result["is_value"] is False


def test_composite_score_keys():
    result = composite_value_score(0.55, 2.0, 3.5, 4.0, "Draw")
    expected_keys = {"outcome", "model_prob", "market_prob", "edge", "ev", "clv", "composite_score", "is_value"}
    assert expected_keys == set(result.keys())


def test_clv_included_when_provided():
    result = composite_value_score(0.55, 2.0, 3.5, 4.0, "Home Win", opening_odds=2.2, closing_odds=2.0)
    assert result["clv"] is not None


def test_clv_none_when_not_provided():
    result = composite_value_score(0.55, 2.0, 3.5, 4.0, "Home Win")
    assert result["clv"] is None
