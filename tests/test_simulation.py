import pytest
from simulation import simulate_league_season, simulate_bets


def test_simulate_season_match_count():
    teams = ["A", "B", "C", "D"]
    df = simulate_league_season(teams)
    assert len(df) == len(teams) * (len(teams) - 1)


def test_simulate_season_columns():
    df = simulate_league_season(["A", "B"])
    assert {"homeTeam", "awayTeam", "homeScore", "awayScore", "date"}.issubset(df.columns)


def test_simulate_season_no_self_play():
    df = simulate_league_season(["A", "B", "C"])
    assert (df["homeTeam"] == df["awayTeam"]).sum() == 0


def test_simulate_bets_count():
    df = simulate_bets(n_bets=50)
    assert len(df) == 50


def test_simulate_bets_balance_changes():
    df = simulate_bets(n_bets=20)
    assert df["balance"].nunique() > 1


def test_simulate_bets_win_rate():
    df = simulate_bets(n_bets=1000, win_rate=0.5, seed=99)
    actual_wr = df["won"].mean()
    assert abs(actual_wr - 0.5) < 0.1
