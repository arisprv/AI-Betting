import pytest
from goal_expectancy import attack_strength, defence_strength, match_xg, expected_goals


def test_attack_strength_average_team():
    assert attack_strength(1.5, 1.5) == pytest.approx(1.0)


def test_attack_strength_strong_team():
    assert attack_strength(2.5, 1.5) > 1.0


def test_defence_strength_average_team():
    assert defence_strength(1.1, 1.1) == pytest.approx(1.0)


def test_match_xg_keys():
    result = match_xg(1.8, 0.8, 1.2, 1.2)
    assert "home_xg" in result
    assert "away_xg" in result
    assert "total_xg" in result


def test_match_xg_strong_home_higher():
    result = match_xg(3.0, 0.5, 0.8, 2.0)
    assert result["home_xg"] > result["away_xg"]


def test_expected_goals_positive():
    xg = expected_goals(1.2, 0.9, 1.5)
    assert xg > 0


def test_total_xg_is_sum(capsys):
    result = match_xg(1.5, 1.0, 1.2, 1.1)
    assert abs(result["total_xg"] - (result["home_xg"] + result["away_xg"])) < 0.01
