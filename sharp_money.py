"""Detect sharp money movement from odds history data."""
import pandas as pd
from odds_history import load_history, detect_steam_move
from logger import get_logger

log = get_logger(__name__)

STEAM_THRESHOLD = 0.08
REVERSE_LINE_THRESHOLD = 0.05


def scan_steam_moves(history_file: str = "odds_history.csv",
                      threshold: float = STEAM_THRESHOLD) -> pd.DataFrame:
    """Scan odds history for steam moves on all matches."""
    df = load_history(history_file)
    if df.empty:
        return pd.DataFrame()

    results = []
    for (home, away), group in df.groupby(["home_team", "away_team"]):
        for market in ["home_odds", "draw_odds", "away_odds"]:
            if market not in group:
                continue
            mkt_hist = group[["snapshot_time", market]].sort_values("snapshot_time")
            is_steam = detect_steam_move(mkt_hist, market=market, threshold=threshold)
            if is_steam:
                first_odds = mkt_hist[market].iloc[0]
                last_odds = mkt_hist[market].iloc[-1]
                results.append({
                    "home_team": home,
                    "away_team": away,
                    "market": market,
                    "opening_odds": first_odds,
                    "current_odds": last_odds,
                    "move_pct": round((first_odds - last_odds) / first_odds * 100, 2),
                })

    log.info("Found %d steam moves", len(results))
    return pd.DataFrame(results)


def reverse_line_movement(public_pct: float, odds_move: float) -> bool:
    """
    Return True if line moved against public betting percentage (reverse line movement).
    public_pct: % of bets on a side (0-1)
    odds_move: fraction by which odds shortened (positive = shortened)
    """
    return public_pct > 0.6 and odds_move < -REVERSE_LINE_THRESHOLD
