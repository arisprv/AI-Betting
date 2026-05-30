import pandas as pd
import pytest
from data_cleaner import drop_null_scores, coerce_score_types, remove_duplicate_matches, clean_matches


def test_drop_null_scores():
    df = pd.DataFrame({
        "homeScore": [2, None, 1],
        "awayScore": [1, 2, None],
    })
    result = drop_null_scores(df)
    assert len(result) == 1


def test_coerce_score_types():
    df = pd.DataFrame({"homeScore": ["2", "1"], "awayScore": ["0", "1"]})
    result = coerce_score_types(df)
    assert result["homeScore"].dtype.name in ("Int64", "int64", "object")


def test_remove_duplicate_matches():
    df = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-01"],
        "homeTeam": ["Arsenal", "Arsenal"],
        "awayTeam": ["Chelsea", "Chelsea"],
        "homeScore": [2, 2],
        "awayScore": [1, 1],
    })
    result = remove_duplicate_matches(df)
    assert len(result) == 1


def test_clean_matches_pipeline():
    df = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-01", "2025-01-08"],
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea"],
        "awayTeam": ["Chelsea", "Chelsea", "Liverpool"],
        "homeScore": ["2", "2", None],
        "awayScore": ["1", "1", "2"],
    })
    result = clean_matches(df)
    assert len(result) == 1
