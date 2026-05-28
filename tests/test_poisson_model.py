import pytest
from poisson_model import score_probabilities, outcome_probs, _poisson_pmf


def test_poisson_pmf_zero():
    p = _poisson_pmf(1.5, 0)
    assert 0 < p < 1


def test_score_probs_sum_to_one():
    probs = score_probabilities(1.5, 1.2)
    total = sum(probs.values())
    assert total == pytest.approx(1.0, abs=0.01)


def test_outcome_probs_sum_to_one():
    probs = outcome_probs(1.5, 1.2)
    total = sum(probs.values())
    assert total == pytest.approx(1.0, abs=0.01)


def test_outcome_probs_keys():
    probs = outcome_probs(1.5, 1.2)
    assert set(probs.keys()) == {"Home Win", "Draw", "Away Win"}


def test_high_home_lambda_favors_home():
    probs = outcome_probs(3.0, 0.5)
    assert probs["Home Win"] > probs["Away Win"]


def test_high_away_lambda_favors_away():
    probs = outcome_probs(0.5, 3.0)
    assert probs["Away Win"] > probs["Home Win"]
