import pandas as pd
import pytest
from feature_store import FeatureStore


@pytest.fixture
def store(tmp_path):
    return FeatureStore(store_dir=str(tmp_path / "features"))


@pytest.fixture
def sample_df():
    return pd.DataFrame({"team": ["Arsenal", "Chelsea"], "win_rate": [0.7, 0.4]})


def test_save_and_load(store, sample_df):
    version = store.save(sample_df, "test_features")
    loaded = store.load("test_features", version)
    assert list(loaded.columns) == list(sample_df.columns)
    assert len(loaded) == len(sample_df)


def test_list_versions(store, sample_df):
    store.save(sample_df, "test_features", version="v1")
    store.save(sample_df, "test_features", version="v2")
    versions = store.list_versions("test_features")
    assert "v1" in versions
    assert "v2" in versions


def test_latest_returns_last(store, sample_df):
    store.save(sample_df, "test_features", version="v1")
    store.save(sample_df, "test_features", version="v2")
    loaded = store.latest("test_features")
    assert len(loaded) == len(sample_df)


def test_load_missing_raises(store):
    with pytest.raises(FileNotFoundError):
        store.load("nonexistent", "v0")
