import pandas as pd
import pytest
from report_generator import generate_text_report


@pytest.fixture
def bets():
    return pd.DataFrame({
        "match": ["Arsenal vs Chelsea", "Liverpool vs Spurs"],
        "prediction": ["Home Win", "Away Win"],
        "stake": [100.0, 50.0],
        "pnl": [80.0, -50.0],
        "won": [True, False],
        "league": ["PL", "PL"],
    })


def test_report_contains_summary(bets):
    report = generate_text_report(bets)
    assert "Summary" in report


def test_report_contains_total_bets(bets):
    report = generate_text_report(bets)
    assert "2" in report


def test_report_contains_league(bets):
    report = generate_text_report(bets)
    assert "By League" in report


def test_report_contains_prediction_type(bets):
    report = generate_text_report(bets)
    assert "By Prediction Type" in report


def test_report_is_string(bets):
    assert isinstance(generate_text_report(bets), str)
