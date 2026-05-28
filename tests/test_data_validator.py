import pandas as pd
import pytest
from data_validator import validate_matches_df, validate_features_df, validate_upcoming_df
from exceptions import DataValidationError


def test_validate_matches_ok():
    df = pd.DataFrame({
        "league": ["PL"],
        "date": ["2025-01-01"],
        "homeTeam": ["Arsenal"],
        "awayTeam": ["Chelsea"],
        "homeScore": [2],
        "awayScore": [1],
    })
    validate_matches_df(df)


def test_validate_matches_missing_column():
    df = pd.DataFrame({"league": ["PL"], "date": ["2025-01-01"]})
    with pytest.raises(DataValidationError):
        validate_matches_df(df)


def test_validate_matches_empty():
    df = pd.DataFrame(columns=["league", "date", "homeTeam", "awayTeam", "homeScore", "awayScore"])
    with pytest.raises(DataValidationError):
        validate_matches_df(df)


def test_validate_matches_null_scores():
    df = pd.DataFrame({
        "league": ["PL"],
        "date": ["2025-01-01"],
        "homeTeam": ["Arsenal"],
        "awayTeam": ["Chelsea"],
        "homeScore": [None],
        "awayScore": [1],
    })
    with pytest.raises(DataValidationError):
        validate_matches_df(df)


def test_validate_features_ok():
    df = pd.DataFrame({
        "team": ["Arsenal"],
        "utcDate": ["2025-01-01"],
        "is_home": [True],
        "avg_goals_5": [1.5],
        "avg_goals_against_5": [0.8],
        "win_rate_5": [0.6],
    })
    validate_features_df(df)


def test_validate_upcoming_missing_column():
    df = pd.DataFrame({"league": ["PL"]})
    with pytest.raises(DataValidationError):
        validate_upcoming_df(df)
