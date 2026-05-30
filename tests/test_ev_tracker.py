import pytest
import os
import tempfile
from expected_value_tracker import record_ev_bet, get_accuracy, ev_accuracy


@pytest.fixture
def tmp_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_record_and_retrieve(tmp_file):
    record_ev_bet("A vs B", predicted_ev=0.12, actual_won=True,
                   odds=2.0, stake=50.0, file=tmp_file)
    acc = ev_accuracy(tmp_file)
    assert acc["count"] == 1


def test_ev_accuracy_empty(tmp_file):
    result = ev_accuracy(tmp_file)
    assert result == {}


def test_multiple_bets(tmp_file):
    for i in range(5):
        record_ev_bet(f"M{i}", 0.1, i % 2 == 0, 2.0, 10.0, file=tmp_file)
    acc = ev_accuracy(tmp_file)
    assert acc["count"] == 5
