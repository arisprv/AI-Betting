import pytest
from multi_market_predictor import full_prediction_card


@pytest.fixture
def card():
    return full_prediction_card("Arsenal", "Chelsea", 1.8, 0.9, 1.2, 1.3)


def test_card_keys(card):
    expected = {"match", "home_xg", "away_xg", "1x2", "over_2_5", "under_2_5",
                "btts_yes", "dnb_home", "dnb_away", "top_scores"}
    assert expected == set(card.keys())


def test_1x2_sums_to_one(card):
    total = sum(card["1x2"].values())
    assert abs(total - 1.0) < 0.01


def test_over_under_sums_to_one(card):
    assert abs(card["over_2_5"] + card["under_2_5"] - 1.0) < 0.01


def test_dnb_sums_to_one(card):
    assert abs(card["dnb_home"] + card["dnb_away"] - 1.0) < 0.01


def test_top_scores_count(card):
    assert len(card["top_scores"]) == 5


def test_match_label(card):
    assert "Arsenal" in card["match"] and "Chelsea" in card["match"]
