import pandas as pd
import pytest
from outlier_detector import total_goals_outliers, goal_diff_outliers, remove_outlier_matches


@pytest.fixture
def normal_matches():
    return pd.DataFrame({
        "homeScore": [1, 2, 1, 2, 1, 1, 2, 1],
        "awayScore": [0, 1, 1, 0, 2, 0, 1, 1],
    })


@pytest.fixture
def matches_with_outlier(normal_matches):
    outlier = pd.DataFrame({"homeScore": [10], "awayScore": [0]})
    return pd.concat([normal_matches, outlier], ignore_index=True)


def test_no_outliers_in_normal_data(normal_matches):
    result = total_goals_outliers(normal_matches, threshold=3.0)
    assert len(result) == 0


def test_detects_high_scoring_outlier(matches_with_outlier):
    result = total_goals_outliers(matches_with_outlier, threshold=2.5)
    assert len(result) >= 1


def test_remove_outlier_reduces_count(matches_with_outlier):
    cleaned = remove_outlier_matches(matches_with_outlier)
    assert len(cleaned) < len(matches_with_outlier)


def test_goal_diff_outlier(matches_with_outlier):
    result = goal_diff_outliers(matches_with_outlier, threshold=2.0)
    assert len(result) >= 1
