import pandas as pd
import pytest
from walk_forward import walk_forward_splits


def test_splits_count():
    df = pd.DataFrame({"utcDate": pd.date_range("2025-01-01", periods=200, freq="D")})
    splits = list(walk_forward_splits(df, n_splits=5, min_train_size=50))
    assert len(splits) == 5


def test_splits_train_before_test():
    df = pd.DataFrame({"utcDate": pd.date_range("2025-01-01", periods=150, freq="D")})
    for train_idx, test_idx in walk_forward_splits(df, n_splits=3, min_train_size=50):
        assert max(train_idx) < min(test_idx)


def test_splits_no_overlap():
    df = pd.DataFrame({"utcDate": pd.date_range("2025-01-01", periods=150, freq="D")})
    for train_idx, test_idx in walk_forward_splits(df, n_splits=3, min_train_size=50):
        assert not set(train_idx) & set(test_idx)
