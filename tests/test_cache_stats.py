import pytest
import data_cache


@pytest.fixture(autouse=True)
def tmp_cache(tmp_path):
    original = data_cache.CACHE_DIR
    data_cache.CACHE_DIR = str(tmp_path / "cache")
    yield
    data_cache.CACHE_DIR = original


def test_cache_stats_empty():
    stats = data_cache.cache_stats()
    assert stats["count"] == 0
    assert stats["size_bytes"] == 0


def test_cache_stats_after_write():
    data_cache.set_cached("http://example.com", {"x": 1}, {})
    stats = data_cache.cache_stats()
    assert stats["count"] == 1
    assert stats["size_bytes"] > 0


def test_cache_stats_after_clear():
    data_cache.set_cached("http://example.com", {"y": 2}, {})
    data_cache.clear_cache()
    stats = data_cache.cache_stats()
    assert stats["count"] == 0
