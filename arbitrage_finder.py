"""Detect arbitrage opportunities across bookmakers."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def arb_margin(home_odds: float, draw_odds: float, away_odds: float) -> float:
    """Return the arbitrage margin (negative = arb exists)."""
    if any(o is None or o <= 0 for o in [home_odds, draw_odds, away_odds]):
        return 0.0
    return (1 / home_odds) + (1 / draw_odds) + (1 / away_odds) - 1.0


def is_arbitrage(home_odds: float, draw_odds: float, away_odds: float) -> bool:
    """Return True if a guaranteed profit exists across these three odds."""
    return arb_margin(home_odds, draw_odds, away_odds) < 0


def optimal_stakes(
    bankroll: float, home_odds: float, draw_odds: float, away_odds: float
) -> dict[str, float]:
    """Return optimal stakes per outcome to guarantee equal profit."""
    margin = 1 / home_odds + 1 / draw_odds + 1 / away_odds
    if margin >= 1:
        return {}
    return {
        "home_stake": round(bankroll / (home_odds * margin), 2),
        "draw_stake": round(bankroll / (draw_odds * margin), 2),
        "away_stake": round(bankroll / (away_odds * margin), 2),
        "guaranteed_profit": round(bankroll / margin - bankroll, 2),
    }


def scan_for_arbs(odds_df: pd.DataFrame) -> pd.DataFrame:
    """Scan a best-odds DataFrame for arbitrage opportunities."""
    arbs = []
    for _, row in odds_df.iterrows():
        ho = row.get("best_home_odds", 0)
        do = row.get("best_draw_odds", 0)
        ao = row.get("best_away_odds", 0)
        if is_arbitrage(ho, do, ao):
            stakes = optimal_stakes(100, ho, do, ao)
            arbs.append({
                "home_team": row.get("home_team"),
                "away_team": row.get("away_team"),
                "home_odds": ho,
                "draw_odds": do,
                "away_odds": ao,
                "margin": round(arb_margin(ho, do, ao), 4),
                **stakes,
            })
    log.info("Found %d arbitrage opportunity(-ies)", len(arbs))
    return pd.DataFrame(arbs)
