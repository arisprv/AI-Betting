import pandas as pd
import pytest
from result_validator import classify_result, validate_predictions


def test_classify_home_win():
    assert classify_result(2, 1) == "Home Win"


def test_classify_draw():
    assert classify_result(1, 1) == "Draw"


def test_classify_away_win():
    assert classify_result(0, 2) == "Away Win"


def test_validate_predictions_correct():
    preds = pd.DataFrame({
        "match": ["Arsenal vs Chelsea"],
        "prediction": ["Home Win"],
        "confidence": [0.65],
    })
    results = pd.DataFrame({
        "match": ["Arsenal vs Chelsea"],
        "homeScore": [2],
        "awayScore": [1],
    })
    validated = validate_predictions(preds, results)
    assert validated["correct"].iloc[0] is True


def test_validate_predictions_incorrect():
    preds = pd.DataFrame({
        "match": ["Arsenal vs Chelsea"],
        "prediction": ["Away Win"],
        "confidence": [0.60],
    })
    results = pd.DataFrame({
        "match": ["Arsenal vs Chelsea"],
        "homeScore": [2],
        "awayScore": [0],
    })
    validated = validate_predictions(preds, results)
    assert validated["correct"].iloc[0] is False


def test_validate_adds_actual_column():
    preds = pd.DataFrame({"match": ["A vs B"], "prediction": ["Draw"], "confidence": [0.55]})
    results = pd.DataFrame({"match": ["A vs B"], "homeScore": [1], "awayScore": [1]})
    validated = validate_predictions(preds, results)
    assert "actual" in validated.columns
