import pandas as pd
import pytest
from odds_analyzer import normalize_overround, expected_value, is_value_bet, best_odds


@pytest.fixture
def sample_odds_df():
    return pd.DataFrame({
        "home_team": ["Arsenal", "Arsenal"],
        "away_team": ["Chelsea", "Chelsea"],
        "bookmaker": ["Bet365", "William Hill"],
        "home_odds": [2.0, 2.1],
        "draw_odds": [3.2, 3.3],
        "away_odds": [3.8, 4.0],
    })


def test_normalize_overround():
    raw = {"Home Win": 2.0, "Draw": 3.5, "Away Win": 4.0}
    normed = normalize_overround(raw)
    assert abs(sum(normed.values()) - 1.0) < 1e-9


def test_expected_value_positive():
    assert expected_value(0.6, 2.0) == pytest.approx(0.2)


def test_expected_value_negative():
    assert expected_value(0.4, 2.0) == pytest.approx(-0.2)


def test_is_value_bet_true():
    assert is_value_bet(0.6, 2.0) is True


def test_is_value_bet_false():
    assert is_value_bet(0.45, 2.0) is False


def test_best_odds_returns_max(sample_odds_df):
    result = best_odds(sample_odds_df, "Arsenal", "Chelsea", "Home Win")
    assert result == pytest.approx(2.1)


def test_best_odds_missing_match(sample_odds_df):
    result = best_odds(sample_odds_df, "Liverpool", "Spurs", "Home Win")
    assert result is None
