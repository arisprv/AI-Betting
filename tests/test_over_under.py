import pytest
from over_under_predictor import over_prob, under_prob, predict_over_under


def test_over_plus_under_equals_one():
    p_over = over_prob(1.5, 1.2, threshold=2.5)
    p_under = under_prob(1.5, 1.2, threshold=2.5)
    assert p_over + p_under == pytest.approx(1.0, abs=1e-6)


def test_high_lambda_over():
    p_over = over_prob(3.0, 3.0, threshold=2.5)
    assert p_over > 0.8


def test_low_lambda_under():
    p_over = over_prob(0.5, 0.5, threshold=2.5)
    assert p_over < 0.3


def test_predict_over_under_keys():
    result = predict_over_under(1.5, 1.2, 1.0, 1.1)
    assert "over_2.5" in result
    assert "under_2.5" in result
    assert "home_xg" in result
    assert "away_xg" in result


def test_predict_over_under_probabilities():
    result = predict_over_under(1.5, 1.2, 1.0, 1.1)
    assert abs(result["over_2.5"] + result["under_2.5"] - 1.0) < 0.01
