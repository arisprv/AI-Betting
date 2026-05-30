"""Export data to various formats: CSV, JSON, and SQLite."""
import json
import pandas as pd
from pathlib import Path
from database import init_db, insert_match, insert_bet
from logger import get_logger

log = get_logger(__name__)


def export_to_csv(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """Export DataFrame to CSV."""
    df.to_csv(path, index=index)
    log.info("Exported %d rows to %s", len(df), path)


def export_to_json(df: pd.DataFrame, path: str, orient: str = "records") -> None:
    """Export DataFrame to JSON."""
    data = df.to_dict(orient=orient)
    Path(path).write_text(json.dumps(data, indent=2, default=str))
    log.info("Exported %d rows to %s", len(df), path)


def export_matches_to_db(matches: pd.DataFrame, db_path: str) -> None:
    """Insert all matches into the SQLite database."""
    init_db(db_path)
    for _, row in matches.iterrows():
        insert_match(
            league=str(row.get("league", "")),
            date=str(row.get("date", row.get("utcDate", ""))),
            home=str(row.get("homeTeam", "")),
            away=str(row.get("awayTeam", "")),
            home_score=int(row.get("homeScore", 0)) if pd.notna(row.get("homeScore")) else None,
            away_score=int(row.get("awayScore", 0)) if pd.notna(row.get("awayScore")) else None,
            db_path=db_path,
        )
    log.info("Exported %d matches to database %s", len(matches), db_path)


def export_bets_to_db(bets: pd.DataFrame, db_path: str) -> None:
    """Insert all bets into the SQLite database."""
    init_db(db_path)
    for _, row in bets.iterrows():
        insert_bet(
            match=str(row.get("match", "")),
            prediction=str(row.get("prediction", "")),
            odds=float(row.get("odds", 0)),
            stake=float(row.get("stake", 0)),
            won=bool(row.get("won", False)),
            pnl=float(row.get("pnl", 0)),
            balance=float(row.get("balance", 0)),
            db_path=db_path,
        )
    log.info("Exported %d bets to database %s", len(bets), db_path)
