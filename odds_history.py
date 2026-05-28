"""Track odds movement over time to detect line movement and steam moves."""
import pandas as pd
from pathlib import Path
from datetime import datetime
from logger import get_logger

log = get_logger(__name__)

HISTORY_FILE = "odds_history.csv"


def record_odds_snapshot(odds_df: pd.DataFrame, file: str = HISTORY_FILE) -> None:
    """Append current odds snapshot with timestamp to a history CSV."""
    snapshot = odds_df.copy()
    snapshot["snapshot_time"] = datetime.now().isoformat()
    exists = Path(file).exists()
    snapshot.to_csv(file, mode="a", header=not exists, index=False)
    log.info("Appended %d odds rows to %s", len(snapshot), file)


def load_history(file: str = HISTORY_FILE) -> pd.DataFrame:
    if not Path(file).exists():
        return pd.DataFrame()
    df = pd.read_csv(file, parse_dates=["snapshot_time"])
    return df


def odds_movement(home: str, away: str, market: str = "home_odds",
                  file: str = HISTORY_FILE) -> pd.DataFrame:
    """Return odds history for a specific match and market."""
    df = load_history(file)
    if df.empty:
        return pd.DataFrame()
    mask = (df["home_team"] == home) & (df["away_team"] == away)
    return df[mask][["snapshot_time", market]].sort_values("snapshot_time")


def detect_steam_move(history: pd.DataFrame, market: str = "home_odds",
                      threshold: float = 0.1) -> bool:
    """Return True if odds dropped by more than threshold (suggesting sharp money)."""
    if len(history) < 2:
        return False
    first = history[market].iloc[0]
    last = history[market].iloc[-1]
    if first == 0:
        return False
    return (first - last) / first > threshold
