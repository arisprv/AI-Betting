"""Match simulation utilities — generate synthetic training data or stress-test strategies."""
import random
import pandas as pd
from datetime import date, timedelta
from logger import get_logger

log = get_logger(__name__)


def simulate_league_season(teams: list[str], avg_home_goals: float = 1.5,
                             avg_away_goals: float = 1.1, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic round-robin season."""
    random.seed(seed)
    import math

    def _poisson(lam: float) -> int:
        L = math.exp(-lam)
        k, p = 0, 1.0
        while p > L:
            k += 1
            p *= random.random()
        return k - 1

    rows = []
    matchday = date(2025, 8, 1)
    for home in teams:
        for away in teams:
            if home == away:
                continue
            hg = _poisson(avg_home_goals)
            ag = _poisson(avg_away_goals)
            rows.append({
                "date": matchday.isoformat(),
                "league": "SIM",
                "homeTeam": home,
                "awayTeam": away,
                "homeScore": hg,
                "awayScore": ag,
            })
            matchday += timedelta(days=3)

    df = pd.DataFrame(rows)
    log.info("Simulated %d matches for %d teams", len(df), len(teams))
    return df


def simulate_bets(n_bets: int = 100, win_rate: float = 0.45,
                  avg_odds: float = 2.0, stake: float = 10.0,
                  seed: int = 42) -> pd.DataFrame:
    """Simulate a sequence of bets for bankroll testing."""
    random.seed(seed)
    records = []
    balance = 1000.0
    for i in range(n_bets):
        won = random.random() < win_rate
        pnl = stake * (avg_odds - 1) if won else -stake
        balance += pnl
        records.append({"bet": i + 1, "won": won, "pnl": pnl, "balance": balance, "stake": stake})
    return pd.DataFrame(records)
