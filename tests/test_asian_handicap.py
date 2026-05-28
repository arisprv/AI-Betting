import pytest
from asian_handicap import asian_handicap_prob, whole_handicap_probs


def test_zero_handicap_sums_to_one():
    result = asian_handicap_prob(1.5, 1.2, 0.0)
    total = result["ah_home"] + result["ah_draw"] + result["ah_away"]
    assert total == pytest.approx(1.0, abs=0.01)


def test_positive_handicap_favors_away():
    result = asian_handicap_prob(1.5, 1.2, -1.5)
    assert result["ah_away"] > result["ah_home"]


def test_whole_handicap_probs_count():
    results = whole_handicap_probs(1.5, 1.2)
    assert len(results) == 7


def test_handicap_values_stored():
    result = asian_handicap_prob(1.5, 1.2, 0.5)
    assert result["handicap"] == 0.5
