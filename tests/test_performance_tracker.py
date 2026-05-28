import pytest
import tempfile
import os
from performance_tracker import record_prediction_outcome, get_accuracy, get_accuracy_by_confidence


@pytest.fixture
def tmp_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_record_and_accuracy(tmp_file):
    record_prediction_outcome("A vs B", "Home Win", "Home Win", 0.65, file=tmp_file)
    record_prediction_outcome("C vs D", "Away Win", "Draw", 0.60, file=tmp_file)
    acc = get_accuracy(tmp_file)
    assert acc == pytest.approx(0.5)


def test_accuracy_empty(tmp_file):
    assert get_accuracy(tmp_file) is None


def test_accuracy_all_correct(tmp_file):
    for i in range(5):
        record_prediction_outcome(f"M{i}", "Home Win", "Home Win", 0.7, file=tmp_file)
    assert get_accuracy(tmp_file) == pytest.approx(1.0)


def test_accuracy_by_confidence(tmp_file):
    record_prediction_outcome("A vs B", "Home Win", "Home Win", 0.75, file=tmp_file)
    record_prediction_outcome("C vs D", "Draw", "Home Win", 0.55, file=tmp_file)
    result = get_accuracy_by_confidence(tmp_file, bins=5)
    assert isinstance(result, dict)
