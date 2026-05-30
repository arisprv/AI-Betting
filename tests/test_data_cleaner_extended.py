import pandas as pd
import pytest
from data_cleaner import remove_duplicate_matches, coerce_score_types


def test_coerce_preserves_valid_ints():
    df = pd.DataFrame({"homeScore": [3, 1], "awayScore": [0, 2]})
    result = coerce_score_types(df)
    assert result["homeScore"].iloc[0] == 3


def test_remove_no_duplicates_unchanged():
    df = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-08"],
        "homeTeam": ["Arsenal", "Chelsea"],
        "awayTeam": ["Chelsea", "Arsenal"],
        "homeScore": [2, 1],
        "awayScore": [1, 2],
    })
    result = remove_duplicate_matches(df)
    assert len(result) == 2


def test_remove_multiple_duplicates():
    df = pd.DataFrame({
        "date": ["2025-01-01"] * 3,
        "homeTeam": ["Arsenal"] * 3,
        "awayTeam": ["Chelsea"] * 3,
        "homeScore": [2, 2, 2],
        "awayScore": [1, 1, 1],
    })
    result = remove_duplicate_matches(df)
    assert len(result) == 1
