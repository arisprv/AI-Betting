import pytest
from value_calculator import composite_value_score


def test_composite_score_scales_with_edge():
    low_edge = composite_value_score(0.52, 2.0, 3.5, 4.0, "Home Win")
    high_edge = composite_value_score(0.70, 2.0, 3.5, 4.0, "Home Win")
    assert high_edge["composite_score"] > low_edge["composite_score"]


def test_away_win_prediction():
    result = composite_value_score(0.60, 2.0, 3.5, 2.5, "Away Win")
    assert "model_prob" in result
    assert result["model_prob"] == pytest.approx(0.60)


def test_draw_prediction():
    result = composite_value_score(0.40, 2.0, 3.5, 4.0, "Draw")
    assert result["outcome"] == "Draw"
