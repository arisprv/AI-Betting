import pytest
from draw_no_bet import dnb_probabilities, dnb_fair_odds


def test_dnb_probs_sum_to_one():
    result = dnb_probabilities(1.5, 1.2)
    assert result["dnb_home"] + result["dnb_away"] == pytest.approx(1.0, abs=0.01)


def test_dnb_draw_prob_positive():
    result = dnb_probabilities(1.5, 1.2)
    assert result["draw_prob"] > 0


def test_dnb_high_lambda_home_favored():
    result = dnb_probabilities(3.0, 0.5)
    assert result["dnb_home"] > result["dnb_away"]


def test_dnb_fair_odds_keys():
    result = dnb_fair_odds(1.5, 1.2)
    assert "dnb_home_odds" in result
    assert "dnb_away_odds" in result


def test_dnb_fair_odds_above_one():
    result = dnb_fair_odds(1.5, 1.2)
    assert result["dnb_home_odds"] > 1.0
    assert result["dnb_away_odds"] > 1.0
