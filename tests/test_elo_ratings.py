import pytest
from elo_ratings import expected_score, update_ratings, DEFAULT_RATING


def test_expected_score_equal_ratings():
    score = expected_score(1500, 1500)
    assert score == pytest.approx(0.5)


def test_expected_score_higher_rating_wins():
    score = expected_score(1600, 1400)
    assert score > 0.5


def test_update_ratings_home_win():
    new_h, new_a = update_ratings(1500, 1500, 2, 1)
    assert new_h > 1500
    assert new_a < 1500


def test_update_ratings_draw():
    new_h, new_a = update_ratings(1500, 1500, 1, 1)
    assert abs(new_h - 1500) < 20
    assert abs(new_a - 1500) < 20


def test_update_ratings_away_win():
    new_h, new_a = update_ratings(1500, 1500, 0, 2)
    assert new_h < 1500
    assert new_a > 1500


def test_ratings_sum_conserved():
    new_h, new_a = update_ratings(1500, 1500, 2, 0)
    assert abs((new_h + new_a) - (1500 + 1500)) < 1e-6
