import pandas as pd
import pytest
from feature_engineering import compute_team_features, _result, _form_score


def test_result_home_win():
    assert _result(2, 1) == 1


def test_result_draw():
    assert _result(1, 1) == 0


def test_result_away_win():
    assert _result(0, 1) == -1


def test_form_score_empty():
    assert _form_score([]) == 0.0


def test_form_score_all_wins():
    score = _form_score([1, 1, 1])
    assert score > 0


def test_form_score_all_losses():
    score = _form_score([-1, -1, -1])
    assert score < 0


def test_form_score_recent_weight():
    score_better_recent = _form_score([-1, -1, 1])
    score_worse_recent = _form_score([1, -1, -1])
    assert score_better_recent > score_worse_recent


@pytest.fixture
def league_df():
    return pd.DataFrame({
        "league": ["PL"] * 6,
        "date": pd.date_range("2025-01-01", periods=6, freq="7D"),
        "homeTeam": ["Arsenal", "Arsenal", "Chelsea", "Arsenal", "Chelsea", "Arsenal"],
        "awayTeam": ["Chelsea", "Liverpool", "Arsenal", "Chelsea", "Liverpool", "Spurs"],
        "homeScore": [2, 1, 1, 3, 0, 2],
        "awayScore": [1, 2, 1, 0, 2, 0],
    })


def test_compute_team_features_returns_records(league_df):
    records = compute_team_features(league_df, "Arsenal", window=5)
    assert len(records) > 0


def test_compute_team_features_has_required_keys(league_df):
    records = compute_team_features(league_df, "Arsenal", window=5)
    for rec in records:
        assert "avg_goals_5" in rec
        assert "win_rate_5" in rec
        assert "form_score_5" in rec


def test_compute_team_features_rolling_window(league_df):
    records = compute_team_features(league_df, "Arsenal", window=2)
    first_with_prev = next((r for r in records if r["avg_goals_5"] > 0), None)
    assert first_with_prev is not None
