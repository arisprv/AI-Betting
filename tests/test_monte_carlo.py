import pytest
from monte_carlo import simulate_match


def test_simulate_match_keys():
    result = simulate_match(1.5, 1.2, n_sims=1000)
    assert set(result.keys()) == {"Home Win", "Draw", "Away Win"}


def test_simulate_match_sums_to_one():
    result = simulate_match(1.5, 1.2, n_sims=1000)
    assert abs(sum(result.values()) - 1.0) < 0.01


def test_simulate_match_high_lambda_favors_home():
    result = simulate_match(3.0, 0.5, n_sims=5000)
    assert result["Home Win"] > result["Away Win"]


def test_simulate_match_low_lambda_more_draws():
    result_low = simulate_match(0.5, 0.5, n_sims=5000)
    result_high = simulate_match(3.0, 3.0, n_sims=5000)
    assert result_low["Draw"] > result_high["Draw"]
