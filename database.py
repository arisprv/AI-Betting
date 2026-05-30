"""SQLite database layer for storing matches, predictions, and bets."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from logger import get_logger

log = get_logger(__name__)

DB_PATH = "football_predictor.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league TEXT NOT NULL,
    date TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    status TEXT DEFAULT 'FINISHED',
    UNIQUE(league, date, home_team, away_team)
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT (datetime('now')),
    match_date TEXT,
    home_team TEXT,
    away_team TEXT,
    prediction TEXT,
    confidence REAL,
    model_version TEXT
);

CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placed_at TEXT DEFAULT (datetime('now')),
    match TEXT,
    prediction TEXT,
    odds REAL,
    stake REAL,
    won INTEGER,
    pnl REAL,
    balance REAL
);
"""


@contextmanager
def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)
    log.info("Database initialised at %s", db_path)


def insert_match(league: str, date: str, home: str, away: str,
                 home_score: int = None, away_score: int = None,
                 db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO matches (league, date, home_team, away_team, home_score, away_score) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (league, date, home, away, home_score, away_score),
        )


def insert_prediction(match_date: str, home: str, away: str, prediction: str,
                       confidence: float, model_version: str = "latest",
                       db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO predictions (match_date, home_team, away_team, prediction, confidence, model_version) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (match_date, home, away, prediction, confidence, model_version),
        )


def insert_bet(match: str, prediction: str, odds: float, stake: float,
               won: bool, pnl: float, balance: float, db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO bets (match, prediction, odds, stake, won, pnl, balance) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (match, prediction, odds, stake, int(won), pnl, balance),
        )
