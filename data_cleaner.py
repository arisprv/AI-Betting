"""Data cleaning utilities for match and feature DataFrames."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def drop_null_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing home or away scores."""
    before = len(df)
    df = df.dropna(subset=["homeScore", "awayScore"])
    log.info("drop_null_scores: removed %d rows", before - len(df))
    return df


def coerce_score_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure homeScore and awayScore are integers."""
    df = df.copy()
    df["homeScore"] = pd.to_numeric(df["homeScore"], errors="coerce").astype("Int64")
    df["awayScore"] = pd.to_numeric(df["awayScore"], errors="coerce").astype("Int64")
    return df


def remove_duplicate_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate matches by (date, homeTeam, awayTeam)."""
    subset = ["date", "homeTeam", "awayTeam"]
    before = len(df)
    df = df.drop_duplicates(subset=subset)
    removed = before - len(df)
    if removed:
        log.warning("Removed %d duplicate match rows", removed)
    return df


def standardise_dates(df: pd.DataFrame, col: str = "date") -> pd.DataFrame:
    """Parse date column to pandas datetime and normalise timezone to UTC-naive."""
    df = df.copy()
    df[col] = pd.to_datetime(df[col], utc=True, errors="coerce").dt.tz_localize(None)
    nulls = df[col].isnull().sum()
    if nulls:
        log.warning("%d rows had unparseable dates in column '%s'", nulls, col)
    return df


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Apply full cleaning pipeline to a raw matches DataFrame."""
    df = coerce_score_types(df)
    df = drop_null_scores(df)
    df = remove_duplicate_matches(df)
    df = standardise_dates(df)
    return df.reset_index(drop=True)
