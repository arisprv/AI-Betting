import pandas as pd
from exceptions import DataValidationError


REQUIRED_MATCH_COLUMNS = {"league", "date", "homeTeam", "awayTeam", "homeScore", "awayScore"}
REQUIRED_FEATURE_COLUMNS = {"team", "utcDate", "is_home", "avg_goals_5", "avg_goals_against_5", "win_rate_5"}
REQUIRED_UPCOMING_COLUMNS = {"league", "utcDate", "homeTeam", "awayTeam"}


def validate_matches_df(df: pd.DataFrame) -> None:
    missing = REQUIRED_MATCH_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Matches DataFrame missing columns: {missing}")
    if df.empty:
        raise DataValidationError("Matches DataFrame is empty")
    if df["homeScore"].isnull().any() or df["awayScore"].isnull().any():
        raise DataValidationError("Matches DataFrame contains null scores")


def validate_features_df(df: pd.DataFrame) -> None:
    missing = REQUIRED_FEATURE_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Features DataFrame missing columns: {missing}")
    if df.empty:
        raise DataValidationError("Features DataFrame is empty")


def validate_upcoming_df(df: pd.DataFrame) -> None:
    missing = REQUIRED_UPCOMING_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Upcoming matches DataFrame missing columns: {missing}")
    if df.empty:
        raise DataValidationError("Upcoming matches DataFrame is empty")