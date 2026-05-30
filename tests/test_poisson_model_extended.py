import pytest
from poisson_model import most_likely_scoreline, estimate_lambda


def test_most_likely_scoreline_returns_tuple():
    score = most_likely_scoreline(1.5, 1.2)
    assert isinstance(score, tuple) and len(score) == 2


def test_most_likely_scoreline_low_scoring():
    score = most_likely_scoreline(0.5, 0.5)
    assert score in [(0, 0), (1, 0), (0, 1)]


def test_estimate_lambda_positive():
    lam = estimate_lambda(1.8, 1.0)
    assert lam > 0


def test_estimate_lambda_league_average_team():
    lam = estimate_lambda(1.5, 1.2, league_avg_home=1.5, league_avg_away=1.2)
    assert lam == pytest.approx(1.5)
