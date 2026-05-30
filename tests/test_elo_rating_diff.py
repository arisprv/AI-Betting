import pytest
from elo_ratings import rating_diff_to_prob


def test_equal_ratings_near_half():
    p = rating_diff_to_prob(1500, 1500)
    assert 0.5 < p < 0.7  # home advantage pushes above 0.5


def test_stronger_home_higher_prob():
    p_strong = rating_diff_to_prob(1700, 1400)
    p_weak = rating_diff_to_prob(1400, 1700)
    assert p_strong > p_weak


def test_prob_range():
    p = rating_diff_to_prob(1600, 1500)
    assert 0.0 <= p <= 1.0
