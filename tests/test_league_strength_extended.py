import pandas as pd
import pytest
from league_strength import competitive_balance


@pytest.fixture
def unbalanced_matches():
    """One team always wins."""
    return pd.DataFrame({
        "league": ["PL"] * 4,
        "homeTeam": ["Arsenal"] * 4,
        "awayTeam": ["A", "B", "C", "D"],
        "homeScore": [3, 3, 3, 3],
        "awayScore": [0, 0, 0, 0],
    })


@pytest.fixture
def balanced_matches():
    """Alternating results."""
    return pd.DataFrame({
        "league": ["PL"] * 4,
        "homeTeam": ["A", "B", "C", "D"],
        "awayTeam": ["B", "C", "D", "A"],
        "homeScore": [1, 0, 1, 0],
        "awayScore": [0, 1, 0, 1],
    })


def test_unbalanced_lower_std(unbalanced_matches, balanced_matches):
    unbal = competitive_balance(unbalanced_matches)["PL"]
    bal = competitive_balance(balanced_matches)["PL"]
    assert unbal < bal or unbal == 0.0
