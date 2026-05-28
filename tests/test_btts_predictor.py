import pytest
from btts_predictor import btts_prob, no_btts_prob, predict_btts


def test_btts_plus_no_btts_equals_one():
    b = btts_prob(1.5, 1.2)
    nb = no_btts_prob(1.5, 1.2)
    assert b + nb == pytest.approx(1.0, abs=1e-6)


def test_high_scoring_increases_btts():
    btts_low = btts_prob(0.5, 0.5)
    btts_high = btts_prob(3.0, 3.0)
    assert btts_high > btts_low


def test_predict_btts_keys():
    result = predict_btts(1.5, 1.2, 1.0, 1.1)
    assert "btts_yes" in result
    assert "btts_no" in result
    assert "home_xg" in result
    assert "away_xg" in result


def test_predict_btts_sums_to_one():
    result = predict_btts(1.5, 1.2, 1.0, 1.1)
    assert abs(result["btts_yes"] + result["btts_no"] - 1.0) < 0.01
