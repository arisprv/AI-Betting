import pandas as pd
import pytest


@pytest.fixture
def sample_matches():
    return pd.DataFrame({
        "league": ["PL"] * 6,
        "date": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "homeTeam": ["Team A", "Team B", "Team A", "Team C", "Team B", "Team A"],
        "awayTeam": ["Team B", "Team C", "Team C", "Team A", "Team A", "Team B"],
        "homeScore": [2, 1, 0, 3, 1, 2],
        "awayScore": [1, 1, 2, 0, 2, 0],
    })


@pytest.fixture
def sample_features():
    return pd.DataFrame({
        "league": ["PL"] * 3,
        "utcDate": pd.date_range("2025-01-08", periods=3, freq="7D"),
        "team": ["Team A", "Team B", "Team C"],
        "is_home": [True, False, True],
        "avg_goals_5": [1.8, 1.2, 2.0],
        "avg_goals_against_5": [0.8, 1.5, 0.6],
        "win_rate_5": [0.6, 0.4, 0.8],
    })
