import pytest
import os
import tempfile
from database import init_db, insert_match, insert_prediction, insert_bet, get_connection


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


def test_init_creates_tables(db_path):
    with get_connection(db_path) as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        names = {t["name"] for t in tables}
    assert "matches" in names
    assert "predictions" in names
    assert "bets" in names


def test_insert_match(db_path):
    insert_match("PL", "2025-01-01", "Arsenal", "Chelsea", 2, 1, db_path)
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM matches").fetchall()
    assert len(rows) == 1


def test_insert_match_idempotent(db_path):
    insert_match("PL", "2025-01-01", "Arsenal", "Chelsea", 2, 1, db_path)
    insert_match("PL", "2025-01-01", "Arsenal", "Chelsea", 2, 1, db_path)
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM matches").fetchall()
    assert len(rows) == 1


def test_insert_prediction(db_path):
    insert_prediction("2025-01-08", "Arsenal", "Chelsea", "Home Win", 0.65, db_path=db_path)
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM predictions").fetchall()
    assert len(rows) == 1


def test_insert_bet(db_path):
    insert_bet("Arsenal vs Chelsea", "Home Win", 2.0, 50.0, True, 50.0, 1050.0, db_path)
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM bets").fetchall()
    assert len(rows) == 1
    assert rows[0]["won"] == 1
