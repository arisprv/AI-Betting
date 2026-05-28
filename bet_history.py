import csv
import os
from datetime import datetime
from pathlib import Path
from logger import get_logger

log = get_logger(__name__)

BET_HISTORY_FILE = "bet_history.csv"
COLUMNS = ["timestamp", "match", "prediction", "confidence", "odds", "stake", "won", "pnl", "balance"]


def append_bet(match: str, prediction: str, confidence: float, odds: float,
               stake: float, won: bool, pnl: float, balance: float,
               file: str = BET_HISTORY_FILE) -> None:
    exists = Path(file).exists()
    with open(file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "match": match,
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "odds": round(odds, 4),
            "stake": round(stake, 2),
            "won": won,
            "pnl": round(pnl, 2),
            "balance": round(balance, 2),
        })


def load_history(file: str = BET_HISTORY_FILE):
    import pandas as pd
    if not Path(file).exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(file, parse_dates=["timestamp"])


def clear_history(file: str = BET_HISTORY_FILE) -> None:
    if Path(file).exists():
        os.remove(file)
        log.info("Cleared bet history: %s", file)
