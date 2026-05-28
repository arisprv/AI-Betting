import pytest
from correct_score_predictor import top_n_scores, most_likely_score


def test_top_n_scores_length():
    results = top_n_scores(1.5, 1.2, n=5)
    assert len(results) == 5


def test_top_n_scores_sorted_descending():
    results = top_n_scores(1.5, 1.2, n=5)
    probs = [p for _, p in results]
    assert probs == sorted(probs, reverse=True)


def test_most_likely_score_is_tuple():
    score = most_likely_score(1.5, 1.2)
    assert isinstance(score, tuple)
    assert len(score) == 2


def test_most_likely_score_high_scoring():
    score = most_likely_score(3.0, 3.0)
    total = score[0] + score[1]
    assert total >= 2


def test_most_likely_score_low_scoring():
    score = most_likely_score(0.5, 0.5)
    assert score in [(0, 0), (1, 0), (0, 1)]
